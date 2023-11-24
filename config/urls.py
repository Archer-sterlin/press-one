from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

...

schema_view = get_schema_view(
    openapi.Info(
        title="Press One API",
        default_version="v1",
        description="Press One API Documentation",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="wistler4u@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path(r"admin/", admin.site.urls),
    path(
        r"",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(r"api/v1/redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path(r"api/v1/", include("items.urls"), name="items-api"),
]
