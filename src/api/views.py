from django.http import JsonResponse
from rest_framework.views import APIView
from datetime import date, timedelta
import pytz
import json
from api.controllers.login_account import LoginController, VerificationController, extract_token, get_user_by_session_token

from api.controllers.login_account import LoginController, VerificationController, UpdatePasswordController

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
                "eatery_id": FieldType.INT,
                "type": FieldType.STRING,
                "content": FieldType.STRING,
            },
        ):
            return JsonResponse(error_json("Malformed Request"))
        CreateReportController(
            eatery_id=EateryID(json_body["eatery_id"]),
            type=json_body["type"],
            content=json_body["content"],
        ).process()
        return JsonResponse(success_json("Reported"))

class LoginView(APIView):
    """Log in given a username and password. Returns session token."""
    def post(self, request):
        json_body = json.loads(request.body)
        if not verify_json_fields(
            json_body,
            {
                "email": FieldType.STRING,
                "password": FieldType.STRING
            },
        ):
            return JsonResponse(error_json("Malformed Request"))

        email = json_body["email"]
        password = json_body["password"]

        try:
            token = LoginController(email, password).process()
            return JsonResponse(success_json(str(token)))

        except Exception as e:
            return JsonResponse(error_json(str(e)))

class TestView(APIView):
    """
    Use for doing things that you need to be logged in for:
    input session token in request header - implies you're already logged in. 
    """
    def post(self, request):
        try:
            session_token = extract_token(request)
            VerificationController(session_token).process()
            return JsonResponse(success_json("accessed successfully!"))
            
        except Exception as e:
            return JsonResponse(error_json(str(e)))

class UpdatePassword(APIView):
    """Change password"""
    def post(self, request):
        json_body = json.loads(request.body)

        if not verify_json_fields(
            json_body,
            {
                "email": FieldType.STRING,
                "old_password":FieldType.STRING,
                "new_password": FieldType.STRING
            },
        ):
            return JsonResponse(error_json("Malformed Request: not password"))
            
        email = json_body["email"]
        old_password = json_body["old_password"]
        new_password = json_body["new_password"]

        try:
            UpdatePasswordController(email, old_password, new_password).process()
            return JsonResponse(success_json("changed password successfully"))

        except Exception as e:
            return JsonResponse(error_json(str(e)))

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
