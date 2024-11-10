from django.urls import path, include
from django.views.decorators.http import require_POST
from user.views import UserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("", UserViewSet)  # Rename to avoid overlap

urlpatterns = [
    path("", include(router.urls)),
]
