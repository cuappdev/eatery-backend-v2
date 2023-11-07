from rest_framework import viewsets
from report.models import Report
from report.serializers import ReportSerializer
from .permissions import ReportPermission
from rest_framework.decorators import action
from rest_framework.response import Response
import os

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [ReportPermission]

    @action(url_path='custom_retrieve',detail=False, methods=['GET'])
    def custom_retrieve(self, request, pk=None):
        if 'key' not in request.headers:
            return Response({"error": "no key"}, status=401)
        if request.headers['key'] != os.environ.get('REPORT_KEY'):
            return Response({"error": "invalid key"}, status=401)
        report = Report.objects.all()
        serializer = ReportSerializer(report, many=True)
        return Response(serializer.data, status=200)