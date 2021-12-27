from django.urls import path

from . import views
from transactions.scripts import ingest_log_transactions

urlpatterns = [
    path("fetch_recent_transactions", views.autofetch_recent_transactions, name="autofetch_recent_transactions"),
    path("mock_vendor_endpoint", views.mock_vendor_endpoint, name="mock_vendor_endpoint"),
    path("ingest_log_transactions", ingest_log_transactions.ingest, name="ingest_log_transactions")
]
