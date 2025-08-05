from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("api/v1/", include("authentication.urls")),
    path("api/v1/", include("customers.urls")),
    path("api/v1/", include("parking.urls")),
    path("api/v1/", include("vehicles.urls")),
    path("", admin.site.urls),
]
