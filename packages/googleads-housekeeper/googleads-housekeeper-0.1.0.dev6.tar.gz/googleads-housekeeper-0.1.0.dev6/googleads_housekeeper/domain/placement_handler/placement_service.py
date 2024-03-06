# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import annotations

import functools
import logging
import operator
from collections import defaultdict
from collections.abc import Iterable
from copy import deepcopy
from dataclasses import dataclass
from typing import Any

import gaarf
import numpy as np
import tenacity
from google.ads import googleads
from google.api_core import exceptions

from googleads_housekeeper import views
from googleads_housekeeper.domain.core import exclusion_specification
from googleads_housekeeper.domain.core import task
from googleads_housekeeper.domain.external_parsers import external_entity_parser
from googleads_housekeeper.domain.placement_handler import entities
from googleads_housekeeper.services import enums
from googleads_housekeeper.services import unit_of_work


@dataclass
class ExclusionResult:
    excluded_placements: int = 0
    associated_with_list_placements: int = 0


class PlacementExcluder:
    """Class for excluding placements based on a sequence of exclusion specifications."""

    associable_with_negative_lists = ('VIDEO',)
    attachable_to_negative_lists = ('DISPLAY', 'SEARCH')

    def __init__(self, client: gaarf.api_clients.GoogleAdsApiClient, uow=None):
        self._client = client
        self.client = client.client
        self.uow = uow

    def exclude_placements(
        self,
        to_be_excluded_placements: gaarf.report.GaarfReport,
        exclusion_level: enums.ExclusionLevelEnum = enums.ExclusionLevelEnum
        .AD_GROUP
    ) -> ExclusionResult:
        """Excludes placements and optionally returns placements which cannot be
    excluded."""
        excluded_placements_count = 0
        associated_placements_count = 0
        self._init_criterion_service_and_operation(exclusion_level)
        report_fetcher = gaarf.query_executor.AdsReportFetcher(self._client)
        customer_ids = to_be_excluded_placements['customer_id'].to_list(
            flatten=True, distinct=True)
        negative_placements_list = report_fetcher.fetch(
            entities.NegativePlacementsLists(), customer_ids)
        (exclusion_operations, shared_set_operations_mapping,
         campaign_set_mapping) = (
             self.
             _create_placement_exclusion_operations_and_non_excluded_placements(
                 to_be_excluded_placements, exclusion_level,
                 negative_placements_list))
        if shared_set_operations_mapping:
            for customer_id, operations in shared_set_operations_mapping.items(
            ):
                try:
                    if operations:
                        self._add_placements_to_shared_set(
                            customer_id, operations)
                        # TODO: provide meaningful message
                        # TODO: display in UI where connection should be made
                        logging.info(
                            'Added %d placements to shared_set for %d account',
                            len(operations), customer_id)
                        associated_placements_count += len(operations)
                except Exception as e:
                    logging.error(e)
        if exclusion_operations:
            for customer_id, operations in exclusion_operations.items():
                try:
                    if operations:
                        self._exclude(customer_id, operations)
                        logging.info('Excluded %d placements from account %s',
                                     len(operations), customer_id)
                        excluded_placements_count += len(operations)
                except Exception as e:
                    logging.error(e)
            logging.info('%d placements was excluded',
                         excluded_placements_count)
        if campaign_set_mapping:
            operations = self._create_campaign_set_operations(
                customer_id, campaign_set_mapping)
            self._add_campaigns_to_shared_set(customer_id, operations)
        return ExclusionResult(
            excluded_placements=excluded_placements_count,
            associated_with_list_placements=associated_placements_count)

    def _init_criterion_service_and_operation(
            self, exclusion_level: enums.ExclusionLevelEnum) -> None:
        # Init services for ShareSets
        self.campaign_service = self.client.get_service('CampaignService')
        self.campaign_set_operation = self.client.get_type(
            'CampaignSharedSetOperation')
        self.shared_set_service = self.client.get_service('SharedSetService')
        self.shared_criterion_service = self.client.get_service(
            'SharedCriterionService')
        self.campaign_shared_set_service = self.client.get_service(
            'CampaignSharedSetService')
        self.shared_set_operation = self.client.get_type('SharedSetOperation')

        if exclusion_level == enums.ExclusionLevelEnum.CAMPAIGN:
            self.criterion_service = self.client.get_service(
                'CampaignCriterionService')
            self.criterion_operation = self.client.get_type(
                'CampaignCriterionOperation')
            self.criterion_path_method = (
                self.criterion_service.campaign_criterion_path)
            self.mutate_operation = (
                self.criterion_service.mutate_campaign_criteria)
            self.entity_name = 'campaign_id'
        if exclusion_level == enums.ExclusionLevelEnum.AD_GROUP:
            self.criterion_service = self.client.get_service(
                'AdGroupCriterionService')
            self.criterion_operation = self.client.get_type(
                'AdGroupCriterionOperation')
            self.criterion_path_method = (
                self.criterion_service.ad_group_criterion_path)
            self.mutate_operation = self.criterion_service.mutate_ad_group_criteria
            self.entity_name = 'ad_group_id'
        if exclusion_level == enums.ExclusionLevelEnum.ACCOUNT:
            self.criterion_service = self.client.get_service(
                'CustomerNegativeCriterionService')
            self.criterion_operation = self.client.get_type(
                'CustomerNegativeCriterionOperation')
            self.criterion_path_method = (
                self.criterion_service.customer_negative_criterion_path)
            self.mutate_operation = (
                self.criterion_service.mutate_customer_negative_criteria)
            self.entity_name = 'customer_id'

    def _create_placement_exclusion_operations_and_non_excluded_placements(
        self, placements: gaarf.report.GaarfReport,
        exclusion_level: enums.ExclusionLevelEnum,
        negative_placements_list: gaarf.report.GaarfReport
    ) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
        """Generates exclusion operations on customer_id level and get all
    placements that cannot be excluded."""
        operations_mapping: dict[str, Any] = {}
        shared_set_operations_mapping: dict[str, Any] = {}
        campaign_set_mapping: dict[str, int] = {}
        allowlisted_placements: dict[int, list[str]] = defaultdict(list)
        with self.uow as uow:
            for allowlisted_placement in uow.allowlisting.list():
                allowlisted_placements[int(
                    allowlisted_placement.account_id)].append(
                        allowlisted_placement.name)

        for placement_info in placements:
            if (placement_info.customer_id in allowlisted_placements and
                    placement_info.placement
                    in allowlisted_placements[placement_info.customer_id]):
                continue
            # TODO: customer_id is not relevant for share_set we need campaign_id
            # TODO: terrible unpacking return object instead
            (customer_id, operation, shared_set,
             is_attachable) = self._create_placement_operation(
                 placement_info, exclusion_level, negative_placements_list)
            if shared_set:
                if isinstance(
                        shared_set_operations_mapping.get(customer_id), list):
                    shared_set_operations_mapping[customer_id].append(operation)
                else:
                    shared_set_operations_mapping[customer_id] = [operation]
                if is_attachable:
                    campaign_set_mapping[
                        shared_set] = placement_info.campaign_id
                continue
            if isinstance(operations_mapping.get(customer_id), list):
                operations_mapping[customer_id].append(operation)
            else:
                operations_mapping[customer_id] = [operation]
        return (operations_mapping, shared_set_operations_mapping,
                campaign_set_mapping)

    def _create_placement_operation(
        self,
        placement_info: gaarf.report.GaarfRow,
        exclusion_level: enums.ExclusionLevelEnum,
        negative_placements_list: gaarf.report.GaarfReport | None = None
    ) -> tuple[str, Any, str, bool]:
        'Creates exclusion operation for a single placement.' ''
        entity_criterion = None
        shared_set_resource_name = None
        is_attachable = False
        if (exclusion_level in (enums.ExclusionLevelEnum.CAMPAIGN,
                                enums.ExclusionLevelEnum.AD_GROUP) and
                placement_info.campaign_type
                in self.associable_with_negative_lists):
            if shared_set_resource_name := self._create_shared_set(
                    placement_info.customer_id, placement_info.campaign_id,
                    negative_placements_list):
                shared_criterion_operation = self.client.get_type(
                    'SharedCriterionOperation')
                entity_criterion = shared_criterion_operation.create
                entity_criterion.shared_set = shared_set_resource_name
            if placement_info.campaign_type in self.attachable_to_negative_lists:
                is_attachable = True

        if (placement_info.placement_type ==
                enums.PlacementTypeEnum.MOBILE_APPLICATION.name):
            app_id = self._format_app_id(placement_info.placement)
        if not entity_criterion:
            entity_criterion = self.criterion_operation.create
        # Assign specific criterion
        if placement_info.placement_type == (
                enums.PlacementTypeEnum.WEBSITE.name):
            entity_criterion.placement.url = placement_info.placement
        if (placement_info.placement_type ==
                enums.PlacementTypeEnum.MOBILE_APPLICATION.name):
            entity_criterion.mobile_application.app_id = app_id
        if placement_info.placement_type == (
                enums.PlacementTypeEnum.YOUTUBE_VIDEO.name):
            entity_criterion.youtube_video.video_id = placement_info.placement
        if (placement_info.placement_type ==
                enums.PlacementTypeEnum.YOUTUBE_CHANNEL.name):
            entity_criterion.youtube_channel.channel_id = (
                placement_info.placement)
        if exclusion_level == enums.ExclusionLevelEnum.ACCOUNT:
            entity_criterion.resource_name = (
                self.criterion_path_method(placement_info.customer_id,
                                           placement_info.criterion_id))
        elif not shared_set_resource_name:
            entity_criterion.negative = True
            entity_criterion.resource_name = (
                self.criterion_path_method(placement_info.customer_id,
                                           placement_info.get(self.entity_name),
                                           placement_info.criterion_id))
        if shared_set_resource_name:
            operation = deepcopy(shared_criterion_operation)
        else:
            operation = deepcopy(self.criterion_operation)
        return (placement_info.customer_id, operation, shared_set_resource_name,
                is_attachable)

    def _create_shared_set(
        self,
        customer_id: int,
        campaign_id: int,
        negative_placements_list: gaarf.report.GaarfReport,
        base_share_set_name: str = 'CPR Negative placements list - Campaign:'
    ) -> str | None:
        name = f'{base_share_set_name} {campaign_id}'
        exclusion_list = negative_placements_list.to_dict(
            key_column='name',
            value_column='resource_name',
            value_column_output='scalar')
        if name in exclusion_list:
            return exclusion_list[name]
        shared_set = self.shared_set_operation.create
        shared_set.name = name
        shared_set.type_ = (
            self.client.enums.SharedSetTypeEnum.NEGATIVE_PLACEMENTS)

        operation = deepcopy(self.shared_set_operation)
        try:
            shared_set_response = self.shared_set_service.mutate_shared_sets(
                customer_id=str(customer_id), operations=[operation])
            shared_set_resource_name = shared_set_response.results[
                0].resource_name
            logging.debug('Created shared set "%s".', shared_set_resource_name)
            return shared_set_resource_name
        except googleads.errors.GoogleAdsException:
            logging.debug('Shared set "%s" already exists.', name)
            return None

    def _add_placements_to_shared_set(self, customer_id: int,
                                      operations: list) -> None:
        if not isinstance(operations, Iterable):
            operations = [operations]
        try:
            for attempt in tenacity.Retrying(
                    retry=tenacity.retry_if_exception_type(
                        exceptions.InternalServerError),
                    stop=tenacity.stop_after_attempt(3),
                    wait=tenacity.wait_exponential()):
                with attempt:
                    self.shared_criterion_service.mutate_shared_criteria(
                        customer_id=str(customer_id), operations=operations)
        except tenacity.RetryError as retry_failure:
            logging.error(
                "Cannot add placements to exclusion list for account '%s' %d times",
                customer_id, retry_failure.last_attempt.attempt_number)

    def _create_campaign_set_operations(self, customer_id,
                                        campaign_set_mapping: dict) -> list:
        campaign_set = self.campaign_set_operation.create
        operations = []
        for shared_set, campaign_id in campaign_set_mapping.items():
            campaign_set.campaign = self.campaign_service.campaign_path(
                customer_id, campaign_id)
            campaign_set.shared_set = shared_set
            operation = deepcopy(self.campaign_set_operation)
            operations.append(operation)
        return operations

    def _add_campaigns_to_shared_set(self, customer_id: str,
                                     operations: list) -> None:
        self.campaign_shared_set_service.mutate_campaign_shared_sets(
            customer_id=str(customer_id), operations=operations)

    def _format_app_id(self, app_id: str) -> str:
        if app_id.startswith('mobileapp::'):
            criteria = app_id.split('-')
            app_id = criteria[-1]
            app_store = criteria[0].split('::')[-1]
            app_store = app_store.replace('mobileapp::1000', '')
            app_store = app_store.replace('1000', '')
            return f'{app_store}-{app_id}'
        return app_id

    def _exclude(self, customer_id: str, operations) -> None:
        """Applies exclusion operations for a single customer_id."""
        if not isinstance(operations, Iterable):
            operations = [operations]
        try:
            for attempt in tenacity.Retrying(
                    retry=tenacity.retry_if_exception_type(
                        exceptions.InternalServerError),
                    stop=tenacity.stop_after_attempt(3),
                    wait=tenacity.wait_exponential()):
                with attempt:
                    self.mutate_operation(
                        customer_id=str(customer_id), operations=operations)
        except tenacity.RetryError as retry_failure:
            logging.error("Cannot exclude placements for account '%s' %d times",
                          customer_id,
                          retry_failure.last_attempt.attempt_number)


def aggregate_placements(
        placements: gaarf.report.GaarfReport,
        exclusion_level: str | enums.ExclusionLevelEnum,
        perform_relative_aggregations: bool = True) -> gaarf.report.GaarfReport:
    """Aggregates placements to a desired exclusion_level.

    By default Placements report returned on Ad Group level, however exclusion
    can be performed on Campaign, Account and MCC level. By aggregating report
    to a desired level exclusion specification can be property applied to
    identify placements that should be excluded.

    Args:
        placements:
            Report with placement related metrics.
        exclusion_level:
            Desired level of aggregation.
        perform_relative_aggregations:
            Whether or not calculate relative metrics (CTR, CPC, etc.)
    Returns:
        Updated report aggregated to desired exclusion level.
    """
    if not isinstance(exclusion_level, enums.ExclusionLevelEnum):
        exclusion_level = getattr(enums.ExclusionLevelEnum, exclusion_level)
    base_groupby = [
        'placement', 'placement_type', 'name', 'criterion_id', 'url'
    ]
    aggregation_dict = dict.fromkeys([
        'clicks',
        'impressions',
        'cost',
        'conversions',
        'video_views',
        'interactions',
        'all_conversions',
        'view_through_conversions',
    ], 'sum')
    relative_aggregations_dict = {
        'ctr': ['clicks', 'impressions'],
        'avg_cpc': ['cost', 'clicks'],
        'avg_cpm': ['cost', 'impressions'],
        'avg_cpv': ['cost', 'video_views'],
        'video_view_rate': ['video_views', 'impressions'],
        'interaction_rate': ['interactions', 'clicks'],
        'conversions_from_interactions_rate': ['conversions', 'interactions'],
        'cost_per_conversion': ['cost', 'conversions'],
        'cost_per_all_conversion': ['cost', 'all_conversions'],
        'all_conversion_rate': ['all_conversions', 'interactions'],
        'all_conversions_from_interactions_rate': [
            'all_conversions', 'interactions'
        ],
    }
    if 'conversion_name' in placements.column_names:
        base_groupby = base_groupby + ['conversion_name']
        aggregation_dict.update(
            dict.fromkeys(['conversions_', 'all_conversions_'], 'sum'))
        relative_aggregations_dict.update({
            'cost_per_conversion_': ['cost', 'conversions_'],
            'cost_per_all_conversion_': ['cost', 'all_conversions_']
        })

    if exclusion_level == enums.ExclusionLevelEnum.ACCOUNT:
        aggregation_groupby = ['account_name', 'customer_id']
    elif exclusion_level == enums.ExclusionLevelEnum.CAMPAIGN:
        aggregation_groupby = [
            'account_name', 'customer_id', 'campaign_id', 'campaign_name',
            'campaign_type'
        ]
    elif exclusion_level == enums.ExclusionLevelEnum.AD_GROUP:
        aggregation_groupby = [
            'account_name', 'customer_id', 'campaign_id', 'campaign_name',
            'campaign_type', 'ad_group_id', 'ad_group_name'
        ]
    groupby = [
        base for base in base_groupby + aggregation_groupby
        if base in placements.column_names
    ]
    aggregations = {
        key: value
        for key, value in aggregation_dict.items()
        if key in placements.column_names
    }
    aggregated_placements = placements.to_pandas().groupby(
        groupby, as_index=False).agg(aggregations)
    if perform_relative_aggregations:
        for key, [numerator, denominator] in relative_aggregations_dict.items():
            if set([numerator,
                    denominator]).issubset(set(aggregated_placements.columns)):
                aggregated_placements[key] = aggregated_placements[
                    numerator] / aggregated_placements[denominator]
                if key == 'avg_cpm':
                    aggregated_placements[
                        key] = aggregated_placements[key] * 1000
                if key == 'ctr':
                    aggregated_placements[key] = round(
                        aggregated_placements[key], 4)
                else:
                    aggregated_placements[key] = round(
                        aggregated_placements[key], 2)
    aggregated_placements.replace([np.inf, -np.inf], 0, inplace=True)
    return gaarf.report.GaarfReport.from_pandas(aggregated_placements)


def join_conversion_split(
        placements: gaarf.report.GaarfReport,
        placements_by_conversion_name: gaarf.report.GaarfReport,
        conversion_name: str) -> gaarf.report.GaarfReport:
    """Joins placements performance data with its conversion split data.

    Args:
        placements:
            Report with placement performance data.
        placements_by_conversion_name:
            Report with placements conversion split data.
        conversion_name:
            Conversion_name(s) that should be used to create a dedicated column
            in joined report.

    Returns:
        New report with extra conversion specific columns.
    """
    placements_by_conversion_name = placements_by_conversion_name.to_pandas()
    final_report_values = []
    for row in placements:
        conversion_row = placements_by_conversion_name.loc[
            (placements_by_conversion_name.ad_group_id == row.ad_group_id)
            & (placements_by_conversion_name.placement == row.placement)]
        data = list(row.data)
        if not (conversions := sum(conversion_row['conversions'].values)):
            conversions = 0.0
        if not (all_conversions := sum(
                conversion_row['all_conversions'].values)):
            all_conversions = 0.0
        data.extend([conversion_name, conversions, all_conversions])
        final_report_values.append(data)
    columns = list(placements.column_names)
    columns.extend(['conversion_name', 'conversions_', 'all_conversions_'])
    return gaarf.report.GaarfReport(
        results=final_report_values, column_names=columns)


def get_placements_for_account(
    account: str, task: task.Task,
    specification: exclusion_specification.ExclusionSpecification,
    report_fetcher: gaarf.query_executor.AdsReportFetcher
) -> gaarf.report.GaarfReport | None:
    runtime_options = specification.define_runtime_options()
    placement_query = entities.Placements(
        placement_types=task.placement_types,
        start_date=task.start_date,
        end_date=task.end_date)
    placements = report_fetcher.fetch(placement_query, customer_ids=account)
    if 'YOUTUBE_VIDEO' in task.placement_types:
        youtube_video_placement_query = entities.Placements(
            placement_types=('YOUTUBE_VIDEO',),
            placement_level_granularity='detail_placement_view',
            start_date=task.start_date,
            end_date=task.end_date)
        youtube_video_placements = report_fetcher.fetch(
            youtube_video_placement_query, customer_ids=account)
        if youtube_video_placements:
            placements = youtube_video_placements + placements

    if not placements:
        return None
    if runtime_options.is_conversion_query:
        conversion_split_query = (
            entities.PlacementsConversionSplit(
                placement_types=task.placement_types,
                start_date=task.start_date,
                end_date=task.end_date))
        placements_by_conversion_name = report_fetcher.fetch(
            conversion_split_query, customer_ids=account)
        if 'YOUTUBE_VIDEO' in task.placement_types:
            youtube_video_conversion_split_query = (
                entities.PlacementsConversionSplit(
                    placement_types=('YOUTUBE_VIDEO',),
                    placement_level_granularity='detail_placement_view',
                    start_date=task.start_date,
                    end_date=task.end_date))
            youtube_video_placements_by_conversion_name = report_fetcher.fetch(
                youtube_video_conversion_split_query, customer_ids=account)
            if youtube_video_placements_by_conversion_name:
                placements_by_conversion_name = (
                    placements_by_conversion_name +
                    youtube_video_placements_by_conversion_name)
        if placements_by_conversion_name:
            conversion_split_exclusion_specification = (
                exclusion_specification.ExclusionSpecification(
                    specifications=[runtime_options.conversion_rules]))
            placements_by_conversion_name = (
                conversion_split_exclusion_specification.apply_specifications(
                    placements_by_conversion_name))
            placements = join_conversion_split(placements,
                                               placements_by_conversion_name,
                                               runtime_options.conversion_name)
    return aggregate_placements(placements, task.exclusion_level)


def find_placements_for_exclusion(
        task: task.Task,
        uow: unit_of_work.AbstractUnitOfWork,
        report_fetcher: gaarf.query_executor.AdsReportFetcher,
        specification: exclusion_specification.ExclusionSpecification
    | None = None,
        always_fetch_youtube_preview_mode: bool = True,
        save_to_db: bool = True) -> gaarf.report.GaarfReport | None:
    external_parser = external_entity_parser.ExternalEntitiesParser(uow)
    ads_specs = specification.ads_specs_entries
    non_ads_specs = specification.non_ads_specs_entries
    reports: list[gaarf.report.GaarfReport] = []
    for account in task.accounts:
        account_allowlisted_placements = views.allowlisted_placements_as_tuples(
            uow, account)
        placements = get_placements_for_account(account, task, specification,
                                                report_fetcher)
        if not placements:
            continue
        if not exclusion_specification:
            if always_fetch_youtube_preview_mode:
                placements = inject_extra_data(placements, uow,
                                               account_allowlisted_placements)
            reports.append(placements)
            continue
        if not non_ads_specs and always_fetch_youtube_preview_mode:
            non_ads_specs = exclusion_specification.ExclusionSpecification(
                specifications=[[
                    exclusion_specification
                    .YouTubeChannelExclusionSpecificationEntry(
                        'subscriberCount > 0')
                ]])

        if ads_specs:
            placements = ads_specs.apply_specifications(
                placements,
                include_reason=False,
                include_matching_placement=False)
            if not placements:
                continue
            # TODO (amarkin): What about not saving to db
        if non_ads_specs:
            external_parser.parse_specification_chain(
                placements,
                non_ads_specs)  # TODO (amarkin): Do we need non_ads_specs here?
            placements = inject_extra_data(placements, uow,
                                           account_allowlisted_placements)
        if (to_be_excluded_placements :=
                specification.apply_specifications(placements)):
            reports.append(to_be_excluded_placements)
    if reports:
        return functools.reduce(operator.add, reports)
    return None


def inject_extra_data(
    placements: gaarf.report.GaarfReport, uow: unit_of_work.AbstractUnitOfWork,
    allowlisted_placements: list[tuple[str, str,
                                       str]]) -> gaarf.report.GaarfReport:
    placement_info_extractor = PlacementInfoExtractor(uow)
    has_allowlisted_placements = allowlisted_placements or False
    for placement in placements:
        if has_allowlisted_placements:
            placement['allowlisting'] = (
                placement.name, placement.placement_type,
                placement.customer_id) in allowlisted_placements
        else:
            placement['allowlisting'] = False
        placement[
            'extra_info'] = placement_info_extractor.extract_placement_info(
                placement)
    return placements


class PlacementInfoExtractor:

    def __init__(self, uow: unit_of_work.AbstractUnitOfWork) -> None:
        self.website_info = uow.website_info
        self.youtube_channel_info = uow.youtube_channel_info
        self.youtube_video_info = uow.youtube_video_info

    def extract_placement_info(self,
                               placement_info: gaarf.report.GaarfRow) -> dict:
        if placement_info.placement_type == 'WEBSITE':
            return {
                'website_info':
                    self._get_placement_from_repo(self.website_info,
                                                  placement_info.placement)
            }
        if placement_info.placement_type == 'YOUTUBE_CHANNEL':
            return {
                'youtube_channel_info':
                    self._get_placement_from_repo(self.youtube_channel_info,
                                                  placement_info.placement)
            }

        if placement_info.placement_type == 'YOUTUBE_VIDEO':
            return {
                'youtube_video_info':
                    self._get_placement_from_repo(self.youtube_video_info,
                                                  placement_info.placement)
            }
        return {}

    def _get_placement_from_repo(self, repo, placement: str) -> dict:
        if placement := repo.get_by_condition('placement', placement):
            return placement[0]
        return {}
