import json
from django.http import JsonResponse
from eatery.datatype.Eatery import EateryID
from rest_framework.views import APIView

from reports.controllers.create_report import CreateReportController
from api.util.json import FieldType, error_json, success_json, verify_json_fields

class ReportView(APIView):
    def post(self, request):
        json_body = json.loads(request.body)
        if not verify_json_fields(
            json_body,
            {
                "eatery_id": FieldType.INT or None,
                "type": FieldType.STRING,
                "content": FieldType.STRING,
            },
            ["eatery_id"],
        ):
            return JsonResponse(error_json("Malformed Request"))

        id_provided = json_body.get("eatery_id")
        CreateReportController(
            type=json_body["type"],
            content=json_body["content"],
            eatery_id=EateryID(id_provided) if id_provided else None,
        ).process()
        return JsonResponse(success_json("Reported"))
