from django.urls import path
from eatery.views import EateryView

from event.views import MainDfgView, ReportView, MenuView, PopulateMenuView

urlpatterns = [
    path("menus/", MenuView.as_view(), name="menu"),
    #path("populate/", PopulateMenu.as_view(), name="populate"),
    #path("<int:eatery_id>/" EateryEvents.as_view(), name="get_events"),
]
