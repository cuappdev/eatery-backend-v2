import json
from datetime import date, timedelta

import pytz
from django.http import JsonResponse
from eatery.datatype.Eatery import EateryID
from rest_framework.views import APIView

from api.dfg.main import main_dfg
from api.util.json import FieldType, error_json, success_json, verify_json_fields

from api.models.MenuModel import MenuStore

# Views for URL Paths are defined here.

class MenuView(APIView):
    model = MenuStore

    def get(self, request):
        queryset = MenuStore.all()
        if queryset is None:
            return JsonResponse(error_json("MenuStore is none"))
        return JsonResponse(queryset)

class MainDfgView(APIView):
    dfg = main_dfg

    def get(self, request):
        tzinfo = pytz.timezone("US/Eastern")
        reload = request.GET.get("reload")
        result = self.dfg(
            tzinfo=tzinfo,
            reload=reload is not None and reload != "false",
            start=date.today(),
            end=date.today() + timedelta(days=7),
        )
        return JsonResponse(result)


