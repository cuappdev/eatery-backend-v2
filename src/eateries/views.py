from django.shortcuts import render
from django.http import JsonResponse
from dfg.datatype.Eatery import EateryID
from eateries.controllers.create_report import CreateReportController
from rest_framework.views import APIView

from util.json import verify_json_fields, success_json, error_json, FieldType
import json
# Create your views here.

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