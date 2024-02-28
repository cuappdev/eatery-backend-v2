from django.urls import path
from report.views import ReportViewSet

reports_list = ReportViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

report_list = ReportViewSet.as_view({
    'get':'retrieve',
    'put':'update',
    'patch':'partial_update',
    'delete':'destroy'
})

urlpatterns = [
    path("", reports_list, name='report-list'),
    path("<int:pk>/", report_list, name='report-list'),
]