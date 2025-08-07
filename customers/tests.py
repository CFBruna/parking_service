import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from .models import Customer


@pytest.fixture
def admin_client():
    user = User.objects.create_user(
        username="admin", password="password", is_staff=True, is_superuser=True
    )
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.mark.django_db
def test_customer_creation():
    customer = Customer.objects.create(name="João Silva", cpf="123.456.789-00")
    assert str(customer) == "João Silva"


@pytest.mark.django_db
def test_customer_api_unauthorized_access():
    client = APIClient()
    response = client.get("/api/v1/customers/")
    assert response.status_code == 403


@pytest.mark.django_db
def test_customer_api_list(admin_client):
    Customer.objects.create(name="Cliente Teste 1")
    response = admin_client.get("/api/v1/customers/")
    assert response.status_code == 200
    assert response.data[0]["name"] == "Cliente Teste 1"


@pytest.mark.django_db
def test_customer_api_create(admin_client):
    payload = {"name": "Novo Cliente", "cpf": "111.222.333-44"}
    response = admin_client.post("/api/v1/customers/", payload, format="json")
    assert response.status_code == 201
    assert Customer.objects.get(cpf="111.222.333-44").name == "Novo Cliente"


@pytest.mark.django_db
def test_customer_api_update(admin_client):
    customer = Customer.objects.create(name="Nome Antigo")
    payload = {"name": "Nome Atualizado"}
    response = admin_client.patch(
        f"/api/v1/customers/{customer.id}/", payload, format="json"
    )
    assert response.status_code == 200
    customer.refresh_from_db()
    assert customer.name == "Nome Atualizado"


@pytest.mark.django_db
def test_customer_api_delete(admin_client):
    customer = Customer.objects.create(name="Para Deletar")
    response = admin_client.delete(f"/api/v1/customers/{customer.id}/")
    assert response.status_code == 204
    assert Customer.objects.count() == 0


@pytest.mark.django_db
def test_staff_can_see_all_customers(admin_client):
    Customer.objects.create(name="Cliente A")
    Customer.objects.create(name="Cliente B")
    response = admin_client.get("/api/v1/customers/")
    assert response.status_code == 200
    assert len(response.data) == 2
