
from django.core.management.base import BaseCommand

from eateries.util import SnapshotFileName

import eateries.serializers as serializers

import json

class Command(BaseCommand):
    help = 'Overrides current state of the db with a db snapshot'

    # Only writes data if the table has been flushed
    def ingest_data(self, serializer, file_name: SnapshotFileName):
        folder_path = "db_snapshots/2022-01-10 13:05:44"
        with open(f"{folder_path}/{file_name.value}", "r") as file:     
            json_objs = []
            for line in file:
                if (len(line) > 2):
                    json_objs.append(json.loads(line))
            serialized_objs = serializer(data=json_objs, many=True)
            serialized_objs.is_valid()
            serialized_objs.save()

    def handle(self, *args, **options):
        self.ingest_data(serializers.EateryStoreSerializer, SnapshotFileName.EATERY_STORE)
        self.ingest_data(serializers.ExceptionStoreSerializer, SnapshotFileName.EXCEPTION_STORE)
        self.ingest_data(serializers.MenuStoreSerializer, SnapshotFileName.MENU_STORE)
        self.ingest_data(serializers.CategoryStoreSerializer, SnapshotFileName.CATEGORY_STORE)
        self.ingest_data(serializers.ItemStoreSerializer, SnapshotFileName.ITEM_STORE)
        self.ingest_data(serializers.SubItemStoreSerializer, SnapshotFileName.SUBITEM_STORE)
        self.ingest_data(serializers.CategoryItemAssociationSerializer, SnapshotFileName.CATEGORY_ITEM_ASSOCIATION)


        # with open(f"{folder_path}/{SnapshotFileName.EXCEPTION_STORE.value}", "r") as file:
        #     serialized_objs = []
        #     for line in file:
        #         if (len(line) > 2):
        #             serialized_objs.append(json.loads(line))
        #     exception_objs = serializers.ExceptionStoreSerializer(data=serialized_objs, many=True)
        #     exception_objs.is_valid()
        #     eatery_objs.save()