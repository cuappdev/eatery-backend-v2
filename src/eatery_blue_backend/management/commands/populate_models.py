from django.core.management.base import BaseCommand
from datetime import datetime
import requests
from eatery.datatype.Eatery import EateryID
from eatery.util.constants import CORNELL_DINING_URL
from event.models import Event
from eatery.controllers.populate_eatery import PopulateEateryController
from event.controllers.populate_event import PopulateEventController
from item.controllers.populate_item import PopulateItemController
from category.controllers.populate_category import PopulateCategoryController
import os
import json


class Command(BaseCommand):
    help = "Populates all models"

    def handle(self, *args, **kwargs):
        self.stdout.write(f"Populating models at {datetime.now()} UTC")
        start = int(datetime.now().timestamp())
        self.process()
        self.stdout.write(
            f"Finished populating models at {datetime.now()} UTC ({int(datetime.now().timestamp()) - start}s)"
        )

    def get_json(self):
        try:
            response = requests.get(CORNELL_DINING_URL, timeout=10)
        except Exception as e:
            raise e
        if response.status_code <= 400:
            response = response.json()
            json_eateries = response["data"]["eateries"]
        return json_eateries
    
    def update_freege_external_eatery(self):
        GOOGLE_SHEETS_API_KEY = os.environ.get("GOOGLE_SHEETS_API_KEY")
        FREEDGE_SHEET_ID = os.environ.get("FREEDGE_SHEET_ID")
        FREEDGE_APPROVED_EMAILS = os.environ.get("FREEDGE_APPROVED_EMAILS")
        if not GOOGLE_SHEETS_API_KEY:
            print("GOOGLE_SHEETS_API_KEY not set, cannot update freege external eatery")
            return
        if not FREEDGE_SHEET_ID:
            print("FREEDGE_SHEET_ID not set, cannot update freege external eatery")
            return
        if not FREEDGE_APPROVED_EMAILS:
            print("FREEDGE_APPROVED_EMAILS not set, cannot update freege external eatery")
            return
        
        approved_emails = FREEDGE_APPROVED_EMAILS.split(",")
        
        try:
            response = requests.get(f"https://sheets.googleapis.com/v4/spreadsheets/{FREEDGE_SHEET_ID}/values/A2:M?key={GOOGLE_SHEETS_API_KEY}", timeout=10)
        except Exception as e:
            raise e
        if response.status_code > 400:
            return
        
        response = response.json()
        freege_items = response["values"]
        
        freege_dining_items = []
        for item in freege_items:
            # item[1] is the email
            # item[4] is item name
            # item[11] is if it is there
            if len(item) < 12:
                continue
            if item[1] not in approved_emails or item[11] != "Yes":
                continue

            freege_dining_items.append({
                "item": item[4].strip(),
                "healthy": False,
                "category": "Free Food",
            })

        with open(
            "./static_sources/external_eateries.json", "w+"
        ) as external_eateries_file:
            external_eateries_json = json.load(external_eateries_file)
            for eatery in external_eateries_json["eateries"]:
                if eatery["id"] == EateryID.FREEDGE.value:
                    print("Updating freege external eatery")
                    eatery["diningItems"] = freege_dining_items
                    break

            json.dump(external_eateries_json, external_eateries_file, indent=2)            

    def logger_wrapper(self, command_obj, log_title, args):
        pre = int(datetime.now().timestamp())
        print(f"{datetime.now()} UTC: {log_title}")
        output = command_obj.process(*args)
        print(f"Done ({int(datetime.now().timestamp()) - pre}s) ")
        return output

    def process(self):
        """
        1. Get JSON from API

        2. create eateries (fron CDN json)

        3. create events (from CDN json)
          return events_dict = { eatery_id : [event, event, event...], eatery_id : ... }

        4. create menus for every eatery's events
          return menus_dict = { eatery_id : [menu, menu, menu...] }

        5. create categories in each menu
          return categories_dict =
            { eatery_id :
              { menu[i] : {"category_name" : id, "category_name" : id...},
                menu[i] : {"category_name" : id...}
              }
            }

        6. create items for each category

        """

        json_eateries = self.get_json()

        self.update_freege_external_eatery()
    
        Event.truncate()

        self.logger_wrapper(
            PopulateEateryController(), "Populating eateries", [json_eateries]
        )

        events_dict = self.logger_wrapper(
            PopulateEventController(), "Populating events", [json_eateries]
        )

        categories_dict = self.logger_wrapper(
            PopulateCategoryController(),
            "Populating categories",
            [events_dict, json_eateries],
        )

        self.logger_wrapper(
            PopulateItemController(),
            "Populating items",
            [categories_dict, json_eateries],
        )

        print("Done populating")
