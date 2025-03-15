# eatery/management/commands/notify_eatery_events.py

from django.core.management.base import BaseCommand
from eatery.util.notifications import push_eatery_data_to_firebase
from datetime import datetime


class Command(BaseCommand):
    help = "Checks for upcoming eatery events and schedules notifications to users"

    def handle(self, *args, **kwargs):
        self.stdout.write(f"Starting firebase data push task at {datetime.now()} UTC")
        push_eatery_data_to_firebase()
        self.stdout.write(
            self.style.SUCCESS("Successfully pushed eatery data to Firebase")
        )
