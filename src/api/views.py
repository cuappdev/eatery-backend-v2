from django.http import JsonResponse
from rest_framework.views import APIView
from datetime import date, timedelta
import pytz
import json

from api.datatype.Eatery import EateryID
from api.dfg.main import main_dfg
from api.controllers.create_report import CreateReportController
from api.controllers.update_eatery import UpdateEateryController
from api.util.json import verify_json_fields, success_json, error_json, FieldType
# Create your views here.


class MainDfgView(APIView):
    dfg = main_dfg

    def get(self, request):
        tzinfo = pytz.timezone("US/Eastern")
        reload = request.GET.get('reload')
        result = self.dfg(
            tzinfo=tzinfo,
            reload=reload is not None and reload != "false",
            start=date.today(),
            end=date.today() + timedelta(days=7)
        )
        return JsonResponse(result)


class ReportView(APIView):
    def post(self, request):
        json_body = json.loads(request.body)
        if not verify_json_fields(json_body, {"eatery_id": FieldType.INT, "type": FieldType.STRING, "content": FieldType.STRING}):
            return JsonResponse(error_json("Malformed Request"))
        CreateReportController(
            eatery_id=EateryID(json_body["eatery_id"]),
            type=json_body["type"],
            content=json_body["content"]
        ).process()
        return JsonResponse(success_json("Reported"))


class UpdateView(APIView):
    def post(self, request):
        text_params = request.POST
        try:
            image_param = request.FILES.get("image")
            print(image_param)
        except:
            image_param = None
        # Will add JSON verification here
        UpdateEateryController(
            text_params.get("id"),
            text_params,
            image_param
        ).process()
        return JsonResponse(success_json("Updated"))
