from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("eatery/", include("eatery.urls")),
    path("event/", include("event.urls")),
    path("item/", include("item.urls")),
    path("category/", include("category.urls")),
    path("report/", include("report.urls")),
]
