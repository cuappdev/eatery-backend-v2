import json
from datetime import date, timedelta

import pytz
from django.http import JsonResponse
from eatery.datatype.Eatery import EateryID
from rest_framework.views import APIView
from rest_framework import generics

from api.dfg.main import main_dfg
from api.util.json import FieldType, error_json, success_json, verify_json_fields

from event.models.MenuModel import MenuStore

class PopulateMenuView(generics.GenericAPIView):
    def get(self, request):

        return JsonResponse(success_json("Populated Menu Models"))

class MenuView(APIView):
    model = MenuStore

    def get(self, request):
        tzinfo = pytz.timezone("US/Eastern") #??
        reload = request.GET.get("reload")
        eatery = request.GET.get("eatery")
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")

        if start_date is None or end_date is None:
            start_date = date.today()
            end_date = date.today() + timedelta(days=7)

        if eatery is not None:
            queryset = MenuStore.objects.filter(eatery = eatery)
        else: 
            queryset = MenuStore.objects.all()
        
        if queryset is None:
            return JsonResponse(error_json("MenuStore is none"))
        return JsonResponse(queryset)


"""class MainDfgView(APIView):
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
"""

