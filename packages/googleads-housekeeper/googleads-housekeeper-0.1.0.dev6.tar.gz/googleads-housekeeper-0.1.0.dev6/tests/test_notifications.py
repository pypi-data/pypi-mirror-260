from __future__ import annotations

import pytest

from googleads_housekeeper.adapters import notifications


class TestNotifications:

    @pytest.fixture
    def payload(self):
        return notifications.MessagePayload(task_name='test_task',
                                            placements_excluded_sample=None,
                                            total_placement_excluded=0,
                                            recipient='test_recipient')

    @pytest.mark.parametrize(
        'notification_type, notification_class',
        [('slack', notifications.SlackNotifications),
         ('email', notifications.GoogleCloudAppEngineEmailNotifications),
         ('console', notifications.ConsoleNotifications),
         ('unknown', notifications.NullNotifications)])
    def test_notification_factory_created_correct_notifications(
            self, notification_type, notification_class):
        notification_service = notifications.NotificationFactory(
        ).create_nofication_service(notification_type=notification_type)
        assert isinstance(notification_service, notification_class)

    def test_sending_notification_through_null_notification_raises_error(
            self, payload):
        notification_service = notifications.NullNotifications(
            notification_type='unknown')
        with pytest.raises(ValueError):
            notification_service.send(payload)
