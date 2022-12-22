from serializers import AlertSerializer
from models import Alert
from django.http import JsonResponse
from api.util.json import FieldType, error_json, success_json, verify_json_fields
from rest_framework.views import APIView
from rest_framework import viewsets 

"""
Basic CRUD functions: 
- create an alert for eatery
- get alert for an eatery
- update an alert for an eatery
- delete alert for an eatery
"""
class AlertView(APIView):
    model = Alert 

    def get(self, request):
        queryset = Alert.objects.all()
        serializer = AlertSerializer(queryset, many=True)
        return JsonResponse(serializer.data)

    def post(self, request):
        pass

    def patch(self, request):
        pass 

    def delete(self, request):
        pass