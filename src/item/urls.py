from django.urls import path, include
from item.views import ItemViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("", ItemViewSet)

urlpatterns = [
    path("", include(router.urls)),
]