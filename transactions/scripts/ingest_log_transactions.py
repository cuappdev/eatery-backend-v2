# Transaction Histories used to be stored in a giant log file. Ingest that log file into the db

import requests
import json
import time
from django.http import JsonResponse

from transactions.controllers.update_transactions_controller import UpdateTransactionsController
from ..models import TransactionHistory

def ingest(request):
    num_deleted = TransactionHistory.objects.all().delete()[0]
    counter = 0
    num_inserted = 0
    with open("static_sources/data.log", "r") as log:
        for line in log:
            try:
                data = json.loads(line)
                timestamp = time.strptime(data['TIMESTAMP'], '%Y-%m-%d %I:%M:%S %p')
                if counter % 100 == 1:
                    print(timestamp)
                if timestamp.tm_year == 2021:
                    counter += 1
                    res = UpdateTransactionsController(data).process()
                    if res["success"]:
                        num_inserted += res["result"]["num_inserted"]
            except:
                # Reading a blank line or INVALID DATE
                pass
    return JsonResponse({
            "success": True,
            "result": {
                "num_inserted": num_inserted,
                "num_deleted": num_deleted
            },
            "error": None
        })