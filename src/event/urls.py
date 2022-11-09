from django.urls import path

from event.views import PopulateEventView, EateryEventsViewSet

urlpatterns = [
    path("populate/", PopulateEventView.as_view(), name="menu"),
    path("<int:eatery_id>/", EateryEventsViewSet.as_view(), name="get_events")
]
