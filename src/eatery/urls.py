from django.urls import path
from eatery.views import PopulateEatery, UpdateEatery, GetEateries


urlpatterns = [
    path("populate/", PopulateEatery.as_view(), name="populate"),
    path("update/", UpdateEatery.as_view(), name="update"),
    path("eateries/", GetEateries.as_view(), name = "get_all"), # Get all eateries + their menu and event information
    #path("eatery/<int:eatery_id>/", Eatery.as_view(), name="get_by"), # Get an eatery by its id. + event serializer
]