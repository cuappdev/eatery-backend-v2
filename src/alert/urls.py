from django.urls import path, include
from rest_framework.routers import DefaultRouter
from alert import views

router = DefaultRouter()
router.register(r'', views.AlertViewSet)

urlpatterns = [
    path('', include(router.urls))
]