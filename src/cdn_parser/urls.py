from django.urls import path 
from cdn_parser.views import PopulateModels

urlpatterns = [
    path("populate/", PopulateModels.as_view(), name="populate")
]