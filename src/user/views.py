from rest_framework import viewsets
from user.models import User
from user.serializers import UserSerializer

class UserViewSet:
    queryset = User.objects.all()
    serializer_class = UserSerializer