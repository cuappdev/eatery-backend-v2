from django.urls import path

from api.views import MainDfgView, UpdatePassword, UpdateView, ReportView, LoginView, TestView

urlpatterns = [
    path("", MainDfgView.as_view(), name="main"),
    path("update", UpdateView.as_view(), name="update"),
    path("report", ReportView.as_view(), name="report"),
    path("login", LoginView.as_view(), name="login"),
    path("changepassword", UpdatePassword.as_view(), name="access"),
    path("testview", TestView.as_view(), name="test")
]
