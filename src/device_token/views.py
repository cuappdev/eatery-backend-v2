from rest_framework import viewsets
from device_token.models import DeviceToken
from device_token.serializers import DeviceTokenSerializer


class DeviceTokenViewSet(viewsets.ModelViewSet):
    queryset = DeviceToken.objects.all()
    serializer_class = DeviceTokenSerializer
