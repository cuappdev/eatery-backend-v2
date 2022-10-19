from django.urls import path
from eatery.views import PopulateEatery, UpdateEatery


urlpatterns = [
    path("populate/", PopulateEatery.as_view(), name="populate"),
    path("update/", UpdateEatery.as_view(), name="update")
]