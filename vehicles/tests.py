import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.test import APIClient

from customers.models import Customer

from .models import Vehicle, VehicleType
from .services import get_or_create_vehicle_with_details


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
def test_vehicletype_model_str():
    vtype = VehicleType.objects.create(name="Caminhão")
    assert str(vtype) == "Caminhão"


@pytest.mark.django_db
def test_service_creates_vehicle_with_faker_data():
    vehicle = get_or_create_vehicle_with_details(license_plate="NEWFAKER1")

    assert vehicle.license_plate == "NEWFAKER1"
    assert vehicle.brand is not None
    assert vehicle.model is not None
    assert vehicle.color is not None
    assert Vehicle.objects.count() == 1


@pytest.mark.django_db
def test_service_updates_existing_vehicle():
    Vehicle.objects.create(license_plate="UPDATE123")
    new_owner = Customer.objects.create(name="Novo Dono")

    updated_vehicle = get_or_create_vehicle_with_details(
        license_plate="UPDATE123", owner_id=new_owner.id
    )

    assert updated_vehicle.owner == new_owner
    updated_vehicle.refresh_from_db()
    assert updated_vehicle.owner == new_owner


@pytest.mark.django_db
def test_service_returns_existing_vehicle():
    vehicle_original = Vehicle.objects.create(
        license_plate="EXIST123", brand="Marca Original"
    )
    returned_vehicle = get_or_create_vehicle_with_details(license_plate="EXIST123")

    assert returned_vehicle.id == vehicle_original.id
    assert returned_vehicle.brand == "Marca Original"


@pytest.mark.django_db
def test_service_requires_license_plate():
    with pytest.raises(ValueError, match="A placa do veículo é obrigatória."):
        get_or_create_vehicle_with_details(license_plate="")


@pytest.mark.django_db
def test_service_raises_error_for_invalid_owner_id():
    with pytest.raises(ObjectDoesNotExist):
        get_or_create_vehicle_with_details(license_plate="INVALIDID", owner_id=999)


@pytest.mark.django_db
def test_api_get_by_plate_creates_new_vehicle(admin_client):
    response = admin_client.post(
        "/api/v1/vehicles/get-by-plate/", {"license_plate": "API-NEW1"}, format="json"
    )
    assert response.status_code == 200
    assert response.data["license_plate"] == "API-NEW1"
    assert Vehicle.objects.filter(license_plate="API-NEW1").exists()


@pytest.mark.django_db
def test_api_get_by_plate_updates_vehicle(admin_client):
    Vehicle.objects.create(license_plate="API-UPD8")
    owner = Customer.objects.create(name="Dono da API")

    response = admin_client.post(
        "/api/v1/vehicles/get-by-plate/",
        {"license_plate": "API-UPD8", "owner": owner.id},
        format="json",
    )
    assert response.status_code == 200
    assert response.data["owner"] == owner.id


@pytest.mark.django_db
def test_api_get_by_plate_handles_bad_request(admin_client):
    response = admin_client.post(
        "/api/v1/vehicles/get-by-plate/", {"license_plate": ""}, format="json"
    )
    assert response.status_code == 400
    assert "error" in response.data


@pytest.mark.django_db
def test_regular_user_can_only_see_their_vehicles(regular_user_client):
    client, user = regular_user_client
    my_customer = Customer.objects.create(name="Eu", user=user)

    Vehicle.objects.create(license_plate="MEU123", owner=my_customer)
    Vehicle.objects.create(license_plate="OUTRO456")

    response_list = client.get("/api/v1/vehicles/")

    assert response_list.status_code == 200
    assert len(response_list.data) == 1
    assert response_list.data[0]["license_plate"] == "MEU123"


@pytest.mark.django_db
def test_api_get_by_plate_handles_invalid_owner_id(admin_client):
    response = admin_client.post(
        "/api/v1/vehicles/get-by-plate/",
        {"license_plate": "API-FAIL", "owner": 999},
        format="json",
    )
    assert response.status_code == 404
    assert "não foi encontrado" in response.data["error"]
