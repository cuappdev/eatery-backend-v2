from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("gs", views.google_sheets_eateries, name="gs")
]
