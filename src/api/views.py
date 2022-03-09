from django.http import JsonResponse
from google_auth_oauthlib import get_user_credentials
from rest_framework.views import APIView
from datetime import date, timedelta
import pytz
import json

from api.datatype.Eatery import EateryID
from api.dfg.main import main_dfg
import api.models.LoginModel
from api.controllers.create_report import CreateReportController
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

class LoginView(APIView):

    model = api.models.LoginModel.LoginStore

    def get(self, request):

        json_body=json.loads(request.body)
        
        if not verify_json_fields(json_body, {"eatery_id": FieldType.INT, "type": FieldType.STRING, "content": FieldType.STRING}):
            return JsonResponse(error_json("Malformed Request"))
        
        username = json_body['username']
        password = json_body['password']

        if username is None or password is None:
            return JsonResponse(error_json("Invalid username or password"))

        #user = get_user_by_username(username)

        

        return JsonResponse(success_json("success"))
