
from django.core.management.base import BaseCommand

from datetime import datetime
from pathlib import Path

from eateries.util import SnapshotFileName

import eateries.models as models
import eateries.serializers as serializers
import pytz
import json

class Command(BaseCommand):
    help = 'Saves the current state of the database'

    def write_to_file(self, serialized_lst, file_path):
        with open(file_path, "w") as file:
            for obj in serialized_lst.data:
                file.write(json.dumps(obj) + "\n")

    def handle(self, *args, **options):
        tzinfo = pytz.timezone("US/Eastern")
        time = datetime.now(tzinfo).strftime("%Y-%m-%d %H:%M:%S")
        folder_path = f"db_snapshots/{time}"
        Path(folder_path).mkdir(parents=True, exist_ok=True)
        
        eateries = models.EateryStore.objects.all()
        self.write_to_file(serializers.EateryStoreSerializer(eateries, many=True), f"{folder_path}/{SnapshotFileName.EATERY_STORE.value}")

        exceptions = models.ExceptionStore.objects.filter(end_timestamp__gte=datetime.now().timestamp())
        self.write_to_file(serializers.ExceptionStoreSerializer(exceptions, many=True), f"{folder_path}/{SnapshotFileName.EXCEPTION_STORE.value}")

        menus = models.MenuStore.objects.all()
        self.write_to_file(serializers.MenuStoreSerializer(menus, many=True), f"{folder_path}/{SnapshotFileName.MENU_STORE.value}")

        categories = models.CategoryStore.objects.all()
        self.write_to_file(serializers.CategoryStoreSerializer(categories, many=True), f"{folder_path}/{SnapshotFileName.CATEGORY_STORE.value}")

        items = models.ItemStore.objects.all()
        self.write_to_file(serializers.ItemStoreSerializer(items, many=True), f"{folder_path}/{SnapshotFileName.ITEM_STORE.value}")

        subitems = models.SubItemStore.objects.all()
        self.write_to_file(serializers.SubItemStoreSerializer(subitems, many=True), f"{folder_path}/{SnapshotFileName.SUBITEM_STORE.value}")

        category_item_associations = models.CategoryItemAssociation.objects.all()
        self.write_to_file(serializers.CategoryItemAssociationSerializer(category_item_associations, many=True), f"{folder_path}/{SnapshotFileName.CATEGORY_ITEM_ASSOCIATION.value}")

        # date_event_schedules = models.DateEventSchedule.objects.filter(canonical_date_gte=datetime.now().date)
        # self.write_to_file(date_event_schedules, f"{folder_path}/{SnapshotFileName.DATE_EVENT_SCHEDULE}")

        # closed_event_schedules = models.ClosedEventSchedule.objects.filter(canonical_date_gte=datetime.now().date)
        # self.write_to_file(closed_event_schedules, f"{folder_path}/{SnapshotFileName.CLOSED_EVENT_SCHEDULE}")

        # day_of_week_event_schedules = models.DayOfWeekEventSchedule.objects.all()
        # self.write_to_file(day_of_week_event_schedules, f"{folder_path}/{SnapshotFileName.DAY_OF_WEEK_EVENT_SCHEDULE}")

        # # TODO: Need to filter here for only the valid schedules
        # event_schedules = models.EventSchedule.objects.all()
        # self.write_to_file(event_schedules, f"{folder_path}/{SnapshotFileName.EVENT_SCHEDULE}")