from django.urls import path, include
from user_session.views import UserSessionViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("", UserSessionViewSet)

urlpatterns = [
    path("", include(router.urls)),
]