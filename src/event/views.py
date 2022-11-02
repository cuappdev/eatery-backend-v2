import json
from datetime import date, timedelta

import pytz
from django.http import JsonResponse
from eatery.datatype.Eatery import EateryID
from rest_framework.views import APIView
from rest_framework import generics

from eatery.util.json import FieldType, error_json, success_json, verify_json_fields

from event.controllers.populate_models import CornellDiningNowController
class PopulateEventView(generics.GenericAPIView):
    def get(self, request):
        try:
            CornellDiningNowController().process()
            return JsonResponse(success_json("Populated EventStore"))
        except Exception as e: 
            return JsonResponse(error_json(str(e)))
