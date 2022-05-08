from django.urls import path
from eatery.views import EateryView

from api.views import MainDfgView, ReportView

urlpatterns = [
    path("", MainDfgView.as_view(), name="main"),
    path("update", EateryView.as_view(), name="update"),
    path("report", ReportView.as_view(), name="report"),
]
