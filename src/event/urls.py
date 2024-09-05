from django.urls import path, include
from event.views import EventViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("", EventViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
