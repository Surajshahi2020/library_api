from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("db/admin/", admin.site.urls),
    path(
        "api/v1/",
        include(
            [
                path("doc/schema/", SpectacularAPIView.as_view(), name="schema"),
                path(
                    "doc/",
                    SpectacularSwaggerView.as_view(url_name="schema"),
                    name="swagger-ui",
                ),
                path(
                    "redoc/",
                    SpectacularRedocView.as_view(url_name="schema"),
                    name="redoc",
                ),
                path("library/", include("apis.urls")),
            ],
        ),
    ),
]
