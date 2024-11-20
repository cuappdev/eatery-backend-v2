from rest_framework import viewsets
from user_session.models import UserSession
from user_session.serializers import UserSessionSerializer


class UserSessionViewSet(viewsets.ModelViewSet):
    queryset = UserSession.objects.all()
    serializer_class = UserSessionSerializer
