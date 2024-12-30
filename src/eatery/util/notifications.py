from datetime import datetime, timedelta
from django.utils import timezone
from user.models import User
from eatery.models import Eatery
from firebase_admin import messaging
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def schedule_event_notifications():
    """
    Schedule notifications for events starting or ending in the next 30 minutes.
    """
    current_time = timezone.now()
    thirty_minutes_later = current_time + timedelta(minutes=30)

    logger.info(f"Running schedule_event_notifications at {current_time}")
    logger.info(f"Checking events happening before {thirty_minutes_later}")

    # Iterate through all eateries and their events
    for eatery in Eatery.objects.all():
        logger.info(f"Checking eatery: {eatery.name}")
        for event in eatery.events.all():
            logger.info(
                f"Checking event: {event.event_description}, start: {event.start}, end: {event.end}"
            )

            start_time = timezone.make_aware(datetime.fromtimestamp(event.start))
            end_time = timezone.make_aware(datetime.fromtimestamp(event.end))

            # Notify users about events starting soon
            if current_time <= start_time <= thirty_minutes_later:
                minutes_to_start = (start_time - current_time).seconds // 60
                logger.info(
                    f"Event '{event.event_description}' is starting in {minutes_to_start} minutes."
                )
                notify_users_about_event(
                    eatery, event, f"in {minutes_to_start} minutes", "starting"
                )

            # Notify users about events ending soon
            if current_time <= end_time <= thirty_minutes_later:
                minutes_to_end = (end_time - current_time).seconds // 60
                logger.info(
                    f"Event '{event.event_description}' is ending in {minutes_to_end} minutes."
                )
                notify_users_about_event(
                    eatery, event, f"in {minutes_to_end} minutes", "ending"
                )


def notify_users_about_event(eatery, event, time_message, action):
    """
    Notify users about a specific event happening at an eatery.

    Args:
        eatery (Eatery): The eatery hosting the event.
        event (dict): The event details (e.g., start and end times, description).
        time_message (str): The time until the event (e.g., "in 15 minutes").
        action (str): The action associated with the notification (e.g., "starting", "ending").
    """
    event_name = event.event_description or "Event"
    message = f"{event_name} at {eatery.name} is {action} {time_message}!"
    logger.info(f"Notification message: '{message}'")

    # Retrieve users who have favorited this eatery
    users_to_notify = User.objects.filter(favorite_eateries__id=eatery.id)
    logger.info(
        f"Found {users_to_notify.count()} users to notify for eatery: {eatery.name}"
    )

    # Send notifications to all devices associated with these users
    for user in users_to_notify:
        user_device_tokens = user.get_fcm_tokens()
        logger.info(f"User {user.netid} has {len(user_device_tokens)} device tokens.")
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
            logger.info(
                f"Successfully sent notification to token {device_token}: {response}"
            )
        except messaging.FirebaseError as e:
            logger.error(f"Firebase error for token {device_token}: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error for token {device_token}: {str(e)}")

    except Exception as e:
        # Log or handle the notification error
        logger.error(
            f"Failed to construct notification for token {device_token}: {str(e)}"
        )
