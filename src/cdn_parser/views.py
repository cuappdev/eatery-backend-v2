from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import generics

from eatery.util.json import FieldType, error_json, success_json, verify_json_fields
from cdn_parser.controllers.populate_models import CornellDiningNowController

class PopulateModels(generics.GenericAPIView):
    def get(self, request):
        CornellDiningNowController().process()
        return JsonResponse(success_json("Populated all models"))

