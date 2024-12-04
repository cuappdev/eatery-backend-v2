from datetime import datetime, timedelta
from django.utils import timezone
from user.models import User, UserFCMDevice
from eatery.models import Eatery


def schedule_event_notifications():
    current_time = timezone.now()
    thirty_minutes_later = current_time + timedelta(minutes=30)

    # Get all events across eateries starting or ending in the next 30 minutes
    for eatery in Eatery.objects.all():
        for event in eatery.events:
            start_time = datetime.fromtimestamp(event["start"])
            end_time = datetime.fromtimestamp(event["end"])

            if current_time <= start_time <= thirty_minutes_later:
                notify_users_about_event(eatery, event, "starting")

            if current_time <= end_time <= thirty_minutes_later:
                notify_users_about_event(eatery, event, "ending")


def notify_users_about_event(eatery, event, action):
    event_name = event["event_description"]
    message = f"{event_name} at {eatery.name} is {action} soon!"

    users_to_notify = User.objects.filter(favorite_eateries__contains=eatery.name)

    for user in users_to_notify:
        user_devices = UserFCMDevice.objects.filter(user=user)
        for device in user_devices:
            device.send_message(
                title=f"Eatery Event {action.capitalize()} Soon", body=message
            )
