# Transaction Histories used to be stored in a giant log file. Ingest that log file into the db

import requests
import os
from requests.structures import CaseInsensitiveDict
from django.core.management.base import BaseCommand
from transactions.controllers.update_transactions_controller import UpdateTransactionsController

class Command(BaseCommand):
    help = 'Fetches transaction data from a vendor API and adds it to our transaction history database'

    def handle(self, *args, **options):
        endpoint = "https://vendor-api-extra.scl.cornell.edu/api/external/location-count"
        headers = CaseInsensitiveDict()
        token = os.environ.get("CORNELL_VENDOR_TOKEN")
        api_key = os.environ.get("CORNELL_VENDOR_API_KEY")
        headers["Accept"] = "application/json"
        headers["Authorization"] = "Bearer {}".format(token)
        headers["X-Api-Key"] = api_key
        resp = requests.get(endpoint, headers=headers)
        num_inserted = 0
        if resp.status_code == 200:
            res = UpdateTransactionsController(resp.json()).process()
            if res["success"]:
                num_inserted = res["result"]["num_inserted"]
        print("{} Entries Inserted".format(num_inserted))