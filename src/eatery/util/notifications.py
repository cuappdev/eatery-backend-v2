from datetime import datetime, timedelta
from django.utils import timezone
from user.models import User
from eatery.models import Eatery
from firebase_admin import messaging


def schedule_event_notifications():
    """
    Schedule notifications for events starting or ending in the next 30 minutes.
    """
    current_time = timezone.now()
    thirty_minutes_later = current_time + timedelta(minutes=30)

    # Iterate through all eateries and their events
    for eatery in Eatery.objects.all():
        for event in eatery.events:
            start_time = datetime.fromtimestamp(event["start"])
            end_time = datetime.fromtimestamp(event["end"])

            # Notify users about events starting soon
            if current_time <= start_time <= thirty_minutes_later:
                notify_users_about_event(eatery, event, "starting")

            # Notify users about events ending soon
            if current_time <= end_time <= thirty_minutes_later:
                notify_users_about_event(eatery, event, "ending")


def notify_users_about_event(eatery, event, action):
    """
    Notify users about a specific event happening at an eatery.

    Args:
        eatery (Eatery): The eatery hosting the event.
        event (dict): The event details (e.g., start and end times, description).
        action (str): The action associated with the notification (e.g., "starting", "ending").
    """
    event_name = event["event_description"]
    message = f"{event_name} at {eatery.name} is {action} soon!"

    # Retrieve users who have favorited this eatery
    users_to_notify = User.objects.filter(favorite_eateries=eatery)

    # Send notifications to all devices associated with these users
    for user in users_to_notify:
        user_device_tokens = user.get_fcm_tokens()
        for token in user_device_tokens:
            send_fcm_notification(token, message, action)


def send_fcm_notification(device_token, message, action):
    """
    Send an FCM notification to a specific device.

    Args:
        device_token (str): The FCM token of the device.
        message (str): The notification message body.
        action (str): The action associated with the notification.
    """
    try:
        # Construct the notification payload
        notification = messaging.Notification(
            title=f"Eatery Event {action.capitalize()} Soon",
            body=message,
        )
        message_payload = messaging.Message(
            notification=notification,
            token=device_token,
        )

        # Send the notification
        try:
            response = messaging.send(message_payload)
            print(f"Successfully sent notification: {response}")
        except messaging.FirebaseError as e:
            print(f"Firebase error: {str(e)}")
        except Exception as e:
            print(f"Unexpected error: {str(e)}")

    except Exception as e:
        # Log or handle the notification error
        print(f"Failed to send notification to {device_token}: {str(e)}")
