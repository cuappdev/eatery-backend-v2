import json
from rest_framework import viewsets
from rest_framework import generics
from person.models import Student, Chef
from person.serializers import StudentSerializer, ChefSerializer, AuthenticateSerializer
from .controllers.authenticate_controller import AuthenticateController

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class ChefViewSet(viewsets.ModelViewSet):
    queryset = Chef.objects.all()
    serializer_class = ChefSerializer

class AuthenticateView(generics.GenericAPIView):
    serializer_class = AuthenticateSerializer

    def post(self, request):
        """Authenticate the current user."""
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            data = request.data
        return AuthenticateController(request, data, self.serializer_class).process()