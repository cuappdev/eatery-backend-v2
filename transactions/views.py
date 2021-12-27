from django.shortcuts import render
from django.http import JsonResponse
from requests.structures import CaseInsensitiveDict
from .controllers.mock_vendor_controller import MockVendorController
from .controllers.update_transactions_controller import UpdateTransactionsController

import requests
import os

def mock_vendor_endpoint(request):
    return JsonResponse(MockVendorController().process())

# Called every 5 minutes, updates TransactionHistory database
def autofetch_recent_transactions(request):
    # endpoint = "https://vendor-api-extra.scl.cornell.edu/api/external/location-count"
    endpoint = "http://localhost:8000/mock_vendor_endpoint"
    headers = CaseInsensitiveDict()
    token = os.environ.get("CORNELL_VENDOR_TOKEN")
    api_key = os.environ.get("CORNELL_VENDOR_API_KEY")
    headers["Accept"] = "application/json"
    headers["Authorization"] = "Bearer {}".format(token)
    headers["X-Api-Key"] = api_key

    resp = requests.get(endpoint, headers=headers)
    if resp.status_code == 200:
        return JsonResponse(UpdateTransactionsController(resp.json()).process())
    else:
        return JsonResponse(UpdateTransactionsController({"error": resp.json()}).process())
    