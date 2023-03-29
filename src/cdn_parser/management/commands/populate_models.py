from django.core.management.base import BaseCommand
from django.utils import timezone
from cdn_parser.controllers.populate_models import CornellDiningNowController
from datetime import datetime

class Command(BaseCommand):
    help = 'Populates all models'
    def handle(self, *args, **kwargs):
      self.stdout.write(f"Populating models at {datetime.now()} UTC")
      start = int(datetime.now().timestamp())
      CornellDiningNowController().process()
      self.stdout.write(f"Populated models ({int(datetime.now().timestamp()) - start}s)")

