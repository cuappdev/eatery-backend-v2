import json
from datetime import date, timedelta

import pytz
from django.http import JsonResponse
from rest_framework.views import APIView

from api.controllers.create_report import CreateReportController
from api.controllers.update_eatery import UpdateEateryController
from api.datatype.Eatery import EateryID
from api.dfg.main import main_dfg
from api.util.json import FieldType, error_json, success_json, verify_json_fields

# Create your views here.


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


class ReportView(APIView):
    def post(self, request):
        json_body = json.loads(request.body)
        if not verify_json_fields(
            json_body,
            {
                "type": FieldType.STRING,
                "content": FieldType.STRING,
            },
        ):
            return JsonResponse(error_json("Malformed Request"))

        id_provided = json_body.get("eatery_id")
        CreateReportController(
            type=json_body["type"],
            content=json_body["content"],
            eatery_id=EateryID(id_provided) if id_provided else None,
        ).process()
        return JsonResponse(success_json("Reported"))


class UpdateView(APIView):
    def post(self, request):
        text_params = request.POST
        try:
            image_param = request.FILES.get("image")
        except:
            image_param = None

        try:
            id = int(text_params.get("id"))
        except:
            return JsonResponse(error_json("ID must be castable to an int"))

        try:
            UpdateEateryController(EateryID(id), text_params, image_param).process()
            return JsonResponse(success_json("Updated"))
        except Exception as e:
            return JsonResponse(error_json(str(e)))
