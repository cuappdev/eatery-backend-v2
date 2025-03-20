from django.utils.timezone import now
from user.models import User
from eatery.models import Eatery
import logging
from eatery_blue_backend.firebase import db
from datetime import timedelta

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def push_eatery_data_to_firebase():
    """
    Push daily eatery and event data to Firebase Firestore.
    Ensure that user device tokens are updated correctly,
    even if there are no new events.
    """
    current_time = now()
    logger.info(f"Pushing eatery data to Firebase at {current_time}")

    eateries_ref = db.collection("eateries")

    for eatery in Eatery.objects.all():
        firestore_eatery_doc = eateries_ref.document(str(eatery.id)).get()
        existing_doc = (
            firestore_eatery_doc.to_dict() if firestore_eatery_doc.exists else {}
        )

        existing_events = existing_doc.get("events", [])
        existing_user_tokens = existing_doc.get("user_tokens", [])

        events = []
        for event in eatery.events.all():
            notify_time_open = event.start - 1800  # 30 minutes before open
            notify_time_close = event.end - 1800  # 30 minutes before close

            is_duplicate = any(
                e["start"] == event.start and e["end"] == event.end
                for e in existing_events
            )
            if is_duplicate:
                logger.info(
                    f"Skipping duplicate event: {event.event_description} at {eatery.name}"
                )
                continue

            events.append(
                {
                    "event_description": event.event_description,
                    "start": event.start,
                    "end": event.end,
                    "notify_time_open": notify_time_open,
                    "notify_time_close": notify_time_close,
                }
            )

        # Retrieve users who favorited this eatery and get their FCM tokens
        users = User.objects.filter(favorite_eateries__id=eatery.id)
        user_tokens = list(
            set(  # Remove duplicates
                token for user in users for token in user.get_fcm_tokens()
            )
        )

        # Check if Firestore should be updated
        should_update = (
            events  # New events exist
            or not firestore_eatery_doc.exists  # Firestore document does not exist
            or set(existing_user_tokens) != set(user_tokens)  # User tokens have changed
        )

        if should_update:
            eateries_ref.document(str(eatery.id)).set(
                {
                    "name": eatery.name,
                    "events": existing_events + events,
                    "user_tokens": user_tokens,
                    "last_updated": current_time.isoformat(),
                }
            )
            logger.info(
                f"Updated Firestore for {eatery.name}: {len(events)} new events, {len(user_tokens)} user tokens."
            )
        else:
            logger.info(
                f"No update needed for {eatery.name} (no new events, no new tokens)."
            )
