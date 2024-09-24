from drf_yasg import openapi
from django.contrib import admin
from django.urls import include, path
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Eatery Blue Backend API Docs",
        default_version="v1",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("eatery/", include("eatery.urls")),
    path("event/", include("event.urls")),
    path("item/", include("item.urls")),
    path("category/", include("category.urls")),
    path("report/", include("report.urls")),
    path("person/", include("person.urls")),
    path("docs/", schema_view.with_ui("swagger", cache_timeout=0)),
]
