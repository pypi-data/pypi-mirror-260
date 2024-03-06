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
"""Contains classes and function to work with Placements from Google Ads API."""
from __future__ import annotations

import dataclasses
import datetime
import uuid

from gaarf import base_query

from googleads_housekeeper.services import enums


class Placements(base_query.BaseQuery):
    """Contains placement meta information and it's performance.

    Placements is a wrapper on BaseQuery that builds GAQL query (located in
    `query_text` attribute) based on provided and validated inputs.
    """

    _today = datetime.datetime.today()
    _start_date = _today - datetime.timedelta(days=7)
    _end_date = _today - datetime.timedelta(days=1)
    _campaign_types = {c.name for c in enums.CampaignTypeEnum}
    _placement_types = {p.name for p in enums.PlacementTypeEnum}
    _non_excludable_placements = ('youtube.com', 'mail.google.com',
                                  'adsenseformobileapps.com')
    _non_supported_campaign_types = ('MULTI_CHANNEL',)

    def __init__(self,
                 placement_types: tuple[str, ...] | None = None,
                 campaign_types: tuple[str, ...] | None = None,
                 placement_level_granularity: str = 'group_placement_view',
                 start_date: str = _start_date.strftime('%Y-%m-%d'),
                 end_date: str = _end_date.strftime('%Y-%m-%d'),
                 clicks: int = 0,
                 cost: int = 0,
                 impressions: int = 0,
                 ctr: float = 1.0):
        """Constructor for the class.

        Args:
            placement_types: List of campaign types that need to be fetched.
            placement_types: List of placement types that need to be fetched
                for exclusion.
            start_date: Start_date of the period.
            end_date: Start_date of the period.
            clicks: Number of clicks for the period.
            impressions: Number of impressions for the period.
            cost: Cost for the period.
            impressions: Impressions for the period.
            ctr: Average CTR for the period.
        """
        if campaign_types:
            if isinstance(campaign_types, str):
                campaign_types = tuple(campaign_types.split(','))
            if (wrong_types :=
                    set(campaign_types).difference(self._campaign_types)):
                raise ValueError('Wrong campaign type(s): ',
                                 ', '.join(wrong_types))
            self.campaign_types = '","'.join(campaign_types)
        else:
            self.campaign_types = '","'.join(self._campaign_types)
        if placement_types:
            if isinstance(placement_types, str):
                placement_types = tuple(placement_types.split(','))
            if (wrong_types :=
                    set(placement_types).difference(self._placement_types)):
                raise ValueError('Wrong placement(s): ', ', '.join(wrong_types))
            self.placement_types = '","'.join(placement_types)
        else:
            self.placement_types = '","'.join(self._placement_types)

        if placement_level_granularity not in ('detail_placement_view',
                                               'group_placement_view'):
            raise ValueError(
                "Only 'detail_placement_view' or 'group_placement_view' "
                'can be specified!')
        self.placement_level_granularity = placement_level_granularity

        self.validate_dates(start_date, end_date)
        self.start_date = start_date
        self.end_date = end_date
        self.non_excludable_placements = '","'.join(
            self._non_excludable_placements)
        self.parent_url = ('group_placement_target_url'
                           if self.placement_level_granularity
                           == 'detail_placement_view' else 'target_url')
        self.query_text = f"""
        SELECT
            customer.descriptive_name AS account_name,
            customer.id AS customer_id,
            campaign.id AS campaign_id,
            campaign.name AS campaign_name,
            campaign.advertising_channel_type AS campaign_type,
            ad_group.id AS ad_group_id,
            ad_group.name AS ad_group_name,
            {self.placement_level_granularity}.{self.parent_url} AS base_url,
            {self.placement_level_granularity}.target_url AS url,
            {self.placement_level_granularity}.placement AS placement,
            {self.placement_level_granularity}.placement_type AS placement_type,
            {self.placement_level_granularity}.resource_name AS resource_name,
            {self.placement_level_granularity}.display_name AS name,
            {self.placement_level_granularity}.resource_name~0 AS criterion_id,
            metrics.clicks AS clicks,
            metrics.impressions AS impressions,
            metrics.cost_micros / 1e6 AS cost,
            metrics.conversions AS conversions,
            metrics.video_views AS video_views,
            metrics.interactions AS interactions,
            metrics.all_conversions AS all_conversions,
            metrics.all_conversions_value AS all_conversions_value,
            metrics.view_through_conversions AS view_through_conversions,
            metrics.conversions_value AS conversions_value
        FROM {self.placement_level_granularity}
        WHERE segments.date >= "{self.start_date}"
            AND segments.date <= "{self.end_date}"
            AND {self.placement_level_granularity}.placement_type IN
                ("{self.placement_types}")
            AND {self.placement_level_granularity}.target_url NOT IN
                ("{self.non_excludable_placements}")
            AND campaign.advertising_channel_type IN ("{self.campaign_types}")
            AND metrics.clicks >= {clicks}
            AND metrics.impressions > {impressions}
            AND metrics.ctr < {ctr}
            AND metrics.cost_micros >= {int(cost*1e6)}
        """

    def validate_dates(self, start_date: str, end_date: str) -> None:
        """Checks whether provides start and end dates are valid."""
        if not self.is_valid_date(start_date):
            raise ValueError(f'Invalid start_date: {start_date}')

        if not self.is_valid_date(end_date):
            raise ValueError(f'Invalid end_date: {end_date}')

        if (datetime.datetime.strptime(start_date, '%Y-%m-%d')
                > datetime.datetime.strptime(end_date, '%Y-%m-%d')):
            raise ValueError('start_date cannot be greater than end_date: '
                             f'{start_date} > {end_date}')

    def is_valid_date(self, date_string: str) -> bool:
        try:
            datetime.datetime.strptime(date_string, '%Y-%m-%d')
            return True
        except ValueError:
            return False


class PlacementsConversionSplit(Placements):
    """Placement conversion performance by each conversion name."""
    _today = datetime.datetime.today()
    _start_date = _today - datetime.timedelta(days=7)
    _end_date = _today - datetime.timedelta(days=1)

    def __init__(
        self,
        placement_types: tuple[str, ...] | None = None,
        campaign_types: tuple[str, ...] | None = None,
        placement_level_granularity: str = 'group_placement_view',
        start_date: str = _start_date.strftime('%Y-%m-%d'),
        end_date: str = _end_date.strftime('%Y-%m-%d')
    ) -> None:
        super().__init__(placement_types, campaign_types,
                         placement_level_granularity, start_date, end_date)
        self.query_text = f"""
        SELECT
            campaign.advertising_channel_type AS campaign_type,
            ad_group.id AS ad_group_id,
            segments.conversion_action_name AS conversion_name,
            {self.placement_level_granularity}.placement AS placement,
            metrics.conversions AS conversions,
            metrics.all_conversions AS all_conversions
        FROM {self.placement_level_granularity}
        WHERE segments.date >= "{self.start_date}"
            AND segments.date <= "{self.end_date}"
            AND {self.placement_level_granularity}.placement_type IN
                ("{self.placement_types}")
            AND {self.placement_level_granularity}.target_url NOT IN
                ("{self.non_excludable_placements}")
            AND campaign.advertising_channel_type IN ("{self.campaign_types}")
        """


class NegativePlacementsLists(base_query.BaseQuery):

    def __init__(self):
        self.query_text = """
            SELECT
                shared_set.name AS name,
                shared_set.resource_name AS resource_name
            FROM shared_set
            WHERE shared_set.type = 'NEGATIVE_PLACEMENTS'
            AND shared_set.status = 'ENABLED'
        """

@dataclasses.dataclass
class AllowlistedPlacement:
    type: enums.PlacementTypeEnum
    name: str
    account_id: str
    id: str = dataclasses.field(default_factory=lambda: str(uuid.uuid4()))
