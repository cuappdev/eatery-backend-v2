import json
from datetime import date, timedelta

import pytz
from django.http import JsonResponse
from eatery.datatype.Eatery import EateryID
from rest_framework.views import APIView
from rest_framework import generics

from eatery.util.json import FieldType, error_json, success_json, verify_json_fields

class PopulateEventView(generics.GenericAPIView):
    pass