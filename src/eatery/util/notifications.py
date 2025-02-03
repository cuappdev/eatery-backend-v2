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
    Include user device tokens for filtering notifications.
    """
    current_time = now()
    logger.info(f"Pushing eatery data to Firebase at {current_time}")

    eateries_ref = db.collection("eateries")

    for eatery in Eatery.objects.all():
        events = [
            {
                "event_description": event.event_description,
                "start": event.start,
                "end": event.end,
                "notify_time_open": event.start - 1800,
                "notify_time_close": event.end - 1800,
            }
            for event in eatery.events.all()
        ]

        users = User.objects.filter(favorite_eateries__id=eatery.id)
        user_tokens = [token for user in users for token in user.get_fcm_tokens()]

        eateries_ref.document(str(eatery.id)).set(
            {
                "name": eatery.name,
                "events": events,
                "user_tokens": user_tokens,
                "last_updated": current_time.isoformat(),
            }
        )
        logger.info(
            f"Pushed data for eatery: {eatery.name} with {len(user_tokens)} tokens"
        )
