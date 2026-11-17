"""Root URL configuration for the autoquiz project."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("concierge.urls")),
    path("admin/", admin.site.urls),
]
