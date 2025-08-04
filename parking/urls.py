from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ParkingRecordViewSet, ParkingSpotViewSet

router = DefaultRouter()
router.register("parking/spots", ParkingSpotViewSet)
router.register("parking/records", ParkingRecordViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
