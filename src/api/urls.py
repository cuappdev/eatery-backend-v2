from django.urls import path

from api.views import MainDfgView, UpdateView, ReportView

urlpatterns = [
    path("", MainDfgView.as_view(), name="main"),
    path("update", UpdateView.as_view(), name="update"),
    path("report", ReportView.as_view(), name="report")
]
