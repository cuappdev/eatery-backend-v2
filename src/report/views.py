from rest_framework import viewsets
from report.models import Report
from report.serializers import ReportSerializer
from .permissions import ReportPermission

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    # permission_classes = [ReportPermission]
    