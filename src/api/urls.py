from django.urls import path

from api.views import MainDfgView, ReportView

urlpatterns = [
    path("", MainDfgView.as_view(), name="main"),
    path("report", ReportView.as_view(), name="report")
]
