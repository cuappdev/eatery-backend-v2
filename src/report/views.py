from rest_framework import viewsets
from report.models import Report
from report.serializers import ReportSerializer
from .permissions import ReportPermission
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
import os

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    # permission_classes = [ReportPermission]
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ReportSerializer(instance)
        return Response(serializer.data)
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = ReportSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )
        # Uses the lookup_field attribute, which defaults to `pk`
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)
        return obj

    # TODO
    def update(self, request, *args, **kwargs):
        # Add request validation - see verify_json_fields in eatery/util/json.py
        pass

    # @action(url_path='custom_retrieve',detail=False, methods=['GET'])
    # def custom_retrieve(self, request, pk=None):
    #     if 'key' not in request.headers:
    #         return Response({"error": "no key"}, status=401)
    #     if request.headers['key'] != os.environ.get('REPORT_KEY'):
    #         return Response({"error": "invalid key"}, status=401)
    #     report = Report.objects.all()
    #     serializer = ReportSerializer(report, many=True)
    #     return Response(serializer.data, status=200)