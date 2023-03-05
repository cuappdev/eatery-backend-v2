from django.urls import path, include
from rest_framework.routers import DefaultRouter
from report import views

router = DefaultRouter()
router.register(r'', views.ReportViewSet)

urlpatterns = [
    path('', include(router.urls))
]