from django.urls import path, include
from device_token.views import DeviceTokenViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("", DeviceTokenViewSet)

urlpatterns = [
    path("", include(router.urls)),
]