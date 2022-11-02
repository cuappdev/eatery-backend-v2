from django.urls import path

from event.views import PopulateEventView

urlpatterns = [
    path("populate/", PopulateEventView.as_view(), name="menu"),
    #path("populate/", PopulateMenu.as_view(), name="populate"),
    #path("<int:eatery_id>/" EateryEvents.as_view(), name="get_events"),
]
