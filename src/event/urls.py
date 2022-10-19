from django.urls import path
from eatery.views import EateryView

from event.views import MainDfgView, ReportView, MenuView

urlpatterns = [
    path("menus", MenuView.as_view(), name="menu"),
    path("populate", PopulateMenu.as_view(), name="populate")
]
