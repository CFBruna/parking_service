import pytest
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.test import APIClient

from vehicles.models import Vehicle

from .models import ParkingRecord, ParkingSpot


@pytest.fixture
def admin_client():
    user = User.objects.create_user(
        username="admin", password="password", is_staff=True, is_superuser=True
    )
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.mark.django_db
def test_parking_spot_model_str():
    spot = ParkingSpot.objects.create(spot_number="A1")
    assert str(spot) == "A1"


@pytest.mark.django_db
def test_parking_spot_api_list(admin_client):
    ParkingSpot.objects.create(spot_number="B2")
    response = admin_client.get("/api/v1/parking/spots/")
    assert response.status_code == 200
    assert len(response.data) > 0
    assert response.data[0]["spot_number"] == "B2"


@pytest.mark.django_db
def test_parking_record_api_create(admin_client):
    spot = ParkingSpot.objects.create(spot_number="C3")
    vehicle = Vehicle.objects.create(license_plate="REC123")
    payload = {"parking_spot": spot.id, "vehicle": vehicle.id}
    response = admin_client.post("/api/v1/parking/records/", payload, format="json")
    assert response.status_code == 201
    assert ParkingRecord.objects.count() == 1


@pytest.mark.django_db
def test_parking_spot_is_occupied_signal():
    spot = ParkingSpot.objects.create(spot_number="A1")
    vehicle = Vehicle.objects.create(license_plate="SIGNAL12")
    assert spot.is_occupied is False
    parking_record = ParkingRecord.objects.create(parking_spot=spot, vehicle=vehicle)
    spot.refresh_from_db()
    assert spot.is_occupied is True
    parking_record.exit_time = timezone.now()
    parking_record.save()
    spot.refresh_from_db()
    assert spot.is_occupied is False
