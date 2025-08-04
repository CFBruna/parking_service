from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import VehicleTypeViewSet, VehicleViewSet

router = DefaultRouter()
router.register("vehicles/type", VehicleTypeViewSet)
router.register("vehicles", VehicleViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
