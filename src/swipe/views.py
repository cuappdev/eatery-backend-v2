from rest_framework import viewsets
from swipe.models import WaitTime
from swipe.serializers import WaitTimeSerializer

class WaitTimeViewSet(viewsets.ModelViewSet):
    queryset = WaitTime.objects.all()
    serializer_class = WaitTimeSerializer