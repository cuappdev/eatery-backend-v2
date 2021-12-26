from django.urls import path

from . import views

urlpatterns = [
    path("fetch_recent_transactions", views.autofetch_recent_transactions, name="autofetch_recent_transactions"),
    path("mock_vendor_endpoint", views.mock_vendor_endpoint, name="mock_vendor_endpoint")
]
