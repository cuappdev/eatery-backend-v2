from django.urls import path, include
from person.views import StudentViewSet, ChefViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("student", StudentViewSet)
router.register("chef", ChefViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
