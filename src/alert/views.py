from rest_framework import viewsets
from alert.models import Alert
from alert.serializers import AlertSerializer
from .permissions import AlertPermission

class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    permission_classes = [AlertPermission]