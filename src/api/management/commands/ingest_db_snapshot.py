
from django.core.management.base import BaseCommand
from api.util.constants import SnapshotFileName
import api.serializers as serializers
import json

class Command(BaseCommand):
    help = 'Overrides current state of the db with a db snapshot. Takes --file argument'

    def add_arguments(self, parser):
        parser.add_argument('--input', type=str)

    # Only writes data if the table has been flushed
    def ingest_data(self, serializer, folder_path: str, file_name: SnapshotFileName):
        with open(f"{folder_path}/{file_name.value}", "r") as file:     
            json_objs = []
            for line in file:
                if (len(line) > 2):
                    json_objs.append(json.loads(line))
            serialized_objs = serializer(data=json_objs, many=True)
            serialized_objs.is_valid()
            serialized_objs.save()

    def handle(self, *args, **options):
        folder_path = options["input"]
        self.ingest_data(serializers.EateryStoreSerializer, folder_path, SnapshotFileName.EATERY_STORE)
        self.ingest_data(serializers.AlertStoreSerializer, folder_path, SnapshotFileName.ALERT_STORE)
        self.ingest_data(serializers.MenuStoreSerializer, folder_path, SnapshotFileName.MENU_STORE)
        self.ingest_data(serializers.CategoryStoreSerializer, folder_path, SnapshotFileName.CATEGORY_STORE)
        self.ingest_data(serializers.ItemStoreSerializer, folder_path, SnapshotFileName.ITEM_STORE)
        self.ingest_data(serializers.SubItemStoreSerializer, folder_path, SnapshotFileName.SUBITEM_STORE)
        self.ingest_data(serializers.CategoryItemAssociationSerializer, folder_path, SnapshotFileName.CATEGORY_ITEM_ASSOCIATION)
        self.ingest_data(serializers.DayOfWeekEventScheduleSerializer, folder_path, SnapshotFileName.DAY_OF_WEEK_EVENT_SCHEDULE)