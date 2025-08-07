import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from customers.models import Customer

from .models import Vehicle, VehicleType


@pytest.fixture
def admin_client():
    user = User.objects.create_user(
        username="admin", password="password", is_staff=True, is_superuser=True
    )
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def regular_user_client():
    user = User.objects.create_user(username="user", password="password")
    client = APIClient()
    client.force_authenticate(user=user)
    return client, user


@pytest.mark.django_db
def test_vehicle_model_str():
    vehicle = Vehicle.objects.create(
        license_plate="TESTE123", brand="Marca Teste", model="Modelo Teste"
    )
    assert str(vehicle) == "TESTE123 - Marca Teste Modelo Teste"


@pytest.mark.django_db
def test_vehicletype_api_create(admin_client):
    payload = {"name": "Motocicleta"}
    response = admin_client.post("/api/v1/vehicles/type/", payload, format="json")
    assert response.status_code == 201
    assert VehicleType.objects.get(name="Motocicleta")


@pytest.mark.django_db
def test_get_by_plate_creates_new_vehicle(admin_client):
    response = admin_client.post(
        "/api/v1/vehicles/get-by-plate/", {"license_plate": "NEW1234"}, format="json"
    )
    assert response.status_code == 200
    assert Vehicle.objects.count() == 1
    assert Vehicle.objects.first().license_plate == "NEW1234"


@pytest.mark.django_db
def test_get_by_plate_preserves_data(admin_client):
    owner = Customer.objects.create(name="Dono Teste")
    v_type = VehicleType.objects.create(name="Carro")
    payload = {"license_plate": "SAVE123", "owner": owner.id, "vehicle_type": v_type.id}
    admin_client.post("/api/v1/vehicles/get-by-plate/", payload, format="json")
    saved_vehicle = Vehicle.objects.get(license_plate="SAVE123")
    assert saved_vehicle.owner == owner
    assert saved_vehicle.vehicle_type == v_type


@pytest.mark.django_db
def test_get_by_plate_updates_existing_vehicle(admin_client):
    Vehicle.objects.create(license_plate="UPDATE12", brand="Marca Antiga")
    new_owner = Customer.objects.create(name="Novo Dono")
    payload = {"license_plate": "UPDATE12", "owner": new_owner.id}
    admin_client.post("/api/v1/vehicles/get-by-plate/", payload, format="json")
    updated_vehicle = Vehicle.objects.get(license_plate="UPDATE12")
    assert updated_vehicle.owner == new_owner


@pytest.mark.django_db
def test_regular_user_can_only_see_their_vehicles(regular_user_client):
    client, user = regular_user_client
    my_customer = Customer.objects.create(name="Eu", user=user)
    my_vehicle = Vehicle.objects.create(license_plate="MEU123", owner=my_customer)
    other_vehicle = Vehicle.objects.create(license_plate="OUTRO456")
    response_list = client.get("/api/v1/vehicles/")
    assert response_list.status_code == 200
    assert len(response_list.data) == 1
    assert response_list.data[0]["license_plate"] == "MEU123"
    response_mine = client.get(f"/api/v1/vehicles/{my_vehicle.id}/")
    assert response_mine.status_code == 200
    response_other = client.get(f"/api/v1/vehicles/{other_vehicle.id}/")
    assert response_other.status_code == 404


@pytest.mark.django_db
def test_vehicletype_model_str():
    vtype = VehicleType.objects.create(name="Caminhão")
    assert str(vtype) == "Caminhão"
