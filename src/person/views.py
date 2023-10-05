from rest_framework import viewsets
from person.models import Student, Chef
from person.serializers import StudentSerializer, ChefSerializer
from .permissions import StudentPermission, ChefPermission

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [StudentPermission]

class ChefViewSet(viewsets.ModelViewSet):
    queryset = Chef.objects.all()
    serializer_class = ChefSerializer
    permission_classes = [ChefPermission]