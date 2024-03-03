from django.urls import path, include
from category.views import CategoryViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("", CategoryViewSet)

urlpatterns = [
    path("", include(router.urls)),
]