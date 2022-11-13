from django.urls import path

from event.views import PopulateEventView

urlpatterns = [
    path("populate/", PopulateEventView.as_view(), name="menu"),
]
