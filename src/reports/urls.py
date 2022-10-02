from django.urls import path
from views import ReportView

urlpatterns = [
    path("", ReportView.as_view(), name="main"),
    """
    path("delete", ReportView.as_view(),name="delete"),
    path("post", ReportView.as_view(), name="post")
    """
]