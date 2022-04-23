from django.urls import path
from eatery.views import UpdateView

from api.views import MainDfgView, ReportView

urlpatterns = [
    path("", MainDfgView.as_view(), name="main"),
    path("update", UpdateView.as_view(), name="update"),
    path("report", ReportView.as_view(), name="report"),
]
