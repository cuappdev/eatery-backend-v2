from django.urls import path 

from alert.views import Alerts

urlpatterns = [
    path("", Alerts.as_view(), name="get_all_alerts"),
    path("<int:eatery_id>/", Alerts.as_view(), name="get_eatery_alerts"),
    path("<int:eatery_id>/edit/", Alerts.as_view(), name="edit_eatery_alerts"),
    path("<int:eatery_id>/edit/<int:alert_id>/", Alerts.as_view(), name="delete_eatery_alert")
]