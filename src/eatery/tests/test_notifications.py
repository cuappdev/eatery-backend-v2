from django.test import TestCase
from unittest.mock import patch, MagicMock
from django.utils.timezone import now
from datetime import timedelta
from eatery.models import Eatery
from event.models import Event
from user.models import User
from eatery.util.notifications import schedule_event_notifications
from device_token.models import DeviceToken


class TestScheduleEventNotifications(TestCase):
    @patch("eatery.util.notifications.send_fcm_notification")
    def test_event_starting_notification(self, mock_send_fcm_notification):
        # Create a mock eatery
        eatery = Eatery.objects.create(
            name="Mock Eatery",
            latitude=42.453527,
            longitude=-76.475944,
        )

        # Create an event starting in 20 minutes
        start_time = int((now() + timedelta(minutes=20.5)).timestamp())
        end_time = int((now() + timedelta(hours=1)).timestamp())
        Event.objects.create(
            eatery=eatery,
            event_description="Breakfast",
            start=start_time,
            end=end_time,
        )

        # Create a mock user and associate them with the eatery
        user = User.objects.create(given_name="Test User", netid="test1")
        user.favorite_eateries.add(eatery)

        # Add a device token for the user
        DeviceToken.objects.create(user=user, device_token="mock_token_1")

        # Call the function
        schedule_event_notifications()

        # Verify that the notification was sent
        mock_send_fcm_notification.assert_called_once()
        called_args = mock_send_fcm_notification.call_args[0]
        expected_time_message = f"in 20 minutes"

        self.assertIn(
            "Breakfast", called_args[1]
        )  # Check the event description in the message
        self.assertIn(
            expected_time_message, called_args[1]
        )  # Check the time in the message
        self.assertIn("opening", called_args[2])  # Check the action in the message

    @patch("eatery.util.notifications.send_fcm_notification")
    def test_event_ending_notification(self, mock_send_fcm_notification):
        # Create a mock eatery
        eatery = Eatery.objects.create(
            name="Mock Eatery",
            latitude=42.453527,
            longitude=-76.475944,
        )

        # Create an event ending in 10 minutes
        start_time = int((now() - timedelta(hours=1)).timestamp())
        end_time = int((now() + timedelta(minutes=10.5)).timestamp())
        Event.objects.create(
            eatery=eatery,
            event_description="Lunch",
            start=start_time,
            end=end_time,
        )

        # Create a mock user who has favorited this eatery
        user = User.objects.create(given_name="Test User 2", netid="test2")
        user.favorite_eateries.add(eatery)

        # Add a device token for the user
        DeviceToken.objects.create(user=user, device_token="mock_token_2")

        # Call the function
        schedule_event_notifications()

        # Verify that the notification was sent
        mock_send_fcm_notification.assert_called_once()
        called_args = mock_send_fcm_notification.call_args[0]
        expected_time_message = f"in 10 minutes"

        self.assertIn(
            "Lunch", called_args[1]
        )  # Check the event description in the message
        self.assertIn(
            expected_time_message, called_args[1]
        )  # Check the time in the message
        self.assertIn("closing", called_args[2])  # Check the action in the message
