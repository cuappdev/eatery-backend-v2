from django.urls import path, reverse_lazy

from api.views import MainDfgView, UpdatePasswordView, RegisterView, PasswordResetRequestView, UpdateView, ReportView, LoginView, TestView

urlpatterns = [
    path("", MainDfgView.as_view(), name="main"),
    path("update", UpdateView.as_view(), name="update"),
    path("report", ReportView.as_view(), name="report"),
    path("login", LoginView.as_view(), name="login"),
    path("password_reset_request", PasswordResetRequestView.as_view(), name="reset_request"),
    path("password_reset/<uidb64>/<token>/", UpdatePasswordView.as_view(), name="reset_confirm"),
    #path("password_reset_success", PasswordChangeSuccessView.as_view(), name="reset_success"),
    path("testview", TestView.as_view(), name="test"),
    path("register", RegisterView.as_view(), name="register"),
]