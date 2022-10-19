from eatery.util.json import FieldType, error_json, success_json, verify_json_fields
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics

from eatery.datatype.Eatery import EateryID

from .controllers.update_eatery import UpdateEateryController
from .controllers.populate_eatery import PopulateEateryController

class PopulateEatery(generics.GenericAPIView):
    def get(self, request):
        """
        Populate Eatery datatable with data from CornellDiningNow
        """
        try: 
            PopulateEateryController().process()
            return JsonResponse(success_json("Populated EateryStore"))
        except Exception as e:
            return JsonResponse(error_json(str(e)))


class UpdateEatery(APIView):
    def post(self, request):
        text_params = request.POST
        if not verify_json_fields(
            text_params,
            {
                "id": FieldType.STRING,
            },
            [
                "name",
                "menu_summary",
                "location",
                "campus_area",
                "online_order_url",
                "latitude",
                "longitude",
                "payment_accepts_meal_swipes",
                "payment_accepts_brbs",
                "payment_accepts_cash",
                "image",
            ],
        ):
            return JsonResponse(error_json("Malformed Request"))

        id = int(text_params.get("id"))
        try:
            image_param = request.FILES.get("image")
        except:
            image_param = None

        try:
            UpdateEateryController(EateryID(id), text_params, image_param).process()
            return JsonResponse(success_json("Updated"))
        except Exception as e:
            return JsonResponse(error_json(str(e)))
