"""
mindtraits/urls.py
Root URL configuration. All API traffic flows through api/urls.py.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("api.urls")),
]
