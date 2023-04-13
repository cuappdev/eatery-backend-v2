from django.urls import path, include
from rest_framework.routers import DefaultRouter
from person import views

router = DefaultRouter()
router.register(r'student', views.StudentViewSet)
router.register(r'chef', views.ChefViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path("authenticate/", views.AuthenticateView.as_view(), name="authenticate"),
]