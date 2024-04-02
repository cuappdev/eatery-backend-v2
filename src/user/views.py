from rest_framework import viewsets
from user.models import User
from user.serializers import UserSerializer
from rest_framework.views import APIView


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SSOViewSet(APIView):
    def post(self, request):
        pass
