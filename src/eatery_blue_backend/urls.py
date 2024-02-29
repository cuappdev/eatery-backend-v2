from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("eatery/", include("eatery.urls")),
    path("report/", include("report.urls")),
    path("person/", include("person.urls")),
]
