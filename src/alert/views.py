from alert.models import AlertStore
from django.http import JsonResponse
from api.util.json import FieldType, error_json, success_json, verify_json_fields
from rest_framework.views import APIView


class AlertView(APIView):
    model = AlertStore 

    def get(self, request):
        queryset = AlertStore.all()
        if queryset is None:
            return JsonResponse(error_json("AlertStore is none"))
        return JsonResponse(queryset)