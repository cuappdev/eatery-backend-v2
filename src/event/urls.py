from django.urls import path
from eatery.views import EateryView

from api.views import MainDfgView, ReportView, MenuView

urlpatterns = [
    path("", MainDfgView.as_view(), name="main"),
    path("menus", MenuView.as_view(), name="menu")
]
