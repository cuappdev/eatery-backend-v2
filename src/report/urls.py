from django.urls import path, include
from report.views import ReportViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register("", ReportViewSet)

urlpatterns = [
    path("", include(router.urls)),
]