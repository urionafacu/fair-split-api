import secrets

import pytest
from django.urls import reverse
from rest_framework import status

from accounts.factories import UserFactory


@pytest.mark.django_db
def test_login(client):
    user = UserFactory()
    token = secrets.token_hex(4)
    payload = {
        "email": user.email,
        "password": "secretpassword",
        "push_token": token,
    }
    response = client.post(
        reverse("token_obtain_pair"),
        data=payload,
    )
    assert response.status_code == status.HTTP_200_OK
    # Test the tokens are present in the response
    data = response.json()
    assert "access" in data
    assert "refresh" in data


@pytest.mark.django_db
def test_login_wrong_email(client):
    token = secrets.token_hex(4)
    payload = {
        "email": "noexiste@ejemplo.com",
        "password": "secretpassword",
        "push_token": token,
    }
    response = client.post(reverse("token_obtain_pair"), data=payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    data = response.json()
    assert "access" not in data and "refresh" not in data


@pytest.mark.django_db
def test_login_wrong_password(client):
    user = UserFactory()
    token = secrets.token_hex(4)
    payload = {
        "email": user.email,
        "password": "incorrecta",
        "push_token": token,
    }
    response = client.post(reverse("token_obtain_pair"), data=payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    data = response.json()
    assert "access" not in data and "refresh" not in data


@pytest.mark.django_db
def test_login_missing_fields(client):
    # Missing password
    user = UserFactory()
    payload = {"email": user.email}
    response = client.post(reverse("token_obtain_pair"), data=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    # Missing email
    payload = {"password": "secretpassword"}
    response = client.post(reverse("token_obtain_pair"), data=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_login_invalid_email_format(client):
    payload = {
        "email": "noesunemail",
        "password": "secretpassword",
    }
    response = client.post(reverse("token_obtain_pair"), data=payload)
    assert response.status_code in (
        status.HTTP_400_BAD_REQUEST,
        status.HTTP_401_UNAUTHORIZED,
    )


@pytest.mark.django_db
def test_login_inactive_user(client):
    user = UserFactory(is_active=False)
    payload = {
        "email": user.email,
        "password": "secretpassword",
    }
    response = client.post(reverse("token_obtain_pair"), data=payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_login_empty_password(client):
    user = UserFactory()
    payload = {
        "email": user.email,
        "password": "",
    }
    response = client.post(reverse("token_obtain_pair"), data=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_login_empty_email(client):
    payload = {
        "email": "",
        "password": "secretpassword",
    }
    response = client.post(reverse("token_obtain_pair"), data=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_login_get_method_not_allowed(client):
    response = client.get(reverse("token_obtain_pair"))
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.django_db
def test_login_with_extra_fields(client):
    user = UserFactory()
    payload = {
        "email": user.email,
        "password": "secretpassword",
        "extra_field": "valor",
    }
    response = client.post(reverse("token_obtain_pair"), data=payload)
    # Should work the same, ignoring the extra field
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access" in data and "refresh" in data


@pytest.mark.django_db
def test_register_user(client):
    payload = {
        "email": "nuevo@ejemplo.com",
        "password": "clave_segura123",
        "first_name": "Nuevo",
        "last_name": "Usuario",
    }
    response = client.post(reverse("users-list"), data=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == payload["email"]
    assert data["first_name"] == payload["first_name"]
    assert data["last_name"] == payload["last_name"]
    assert "password" not in data


@pytest.mark.django_db
def test_register_user_duplicate_email(client):
    user = UserFactory()
    payload = {
        "email": user.email,
        "password": "otra_clave123",
        "first_name": "Repetido",
        "last_name": "Usuario",
    }
    response = client.post(reverse("users-list"), data=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    data = response.json()
    assert "email" in data


@pytest.mark.django_db
def test_register_user_invalid_email(client):
    payload = {
        "email": "noesunemail",
        "password": "clave_segura123",
        "first_name": "Nuevo",
        "last_name": "Usuario",
    }
    response = client.post(reverse("users-list"), data=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    data = response.json()
    assert "email" in data


@pytest.mark.django_db
def test_register_user_missing_fields(client):
    # Missing email
    payload = {
        "password": "clave_segura123",
        "first_name": "Nuevo",
        "last_name": "Usuario",
    }
    response = client.post(reverse("users-list"), data=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    # Missing password
    payload = {
        "email": "nuevo2@ejemplo.com",
        "first_name": "Nuevo",
        "last_name": "Usuario",
    }
    response = client.post(reverse("users-list"), data=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_register_user_empty_password(client):
    payload = {
        "email": "nuevo3@ejemplo.com",
        "password": "",
        "first_name": "Nuevo",
        "last_name": "Usuario",
    }
    response = client.post(reverse("users-list"), data=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    data = response.json()
    assert "password" in data


@pytest.mark.django_db
def test_register_user_empty_email(client):
    payload = {
        "email": "",
        "password": "clave_segura123",
        "first_name": "Nuevo",
        "last_name": "Usuario",
    }
    response = client.post(reverse("users-list"), data=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    data = response.json()
    assert "email" in data


@pytest.mark.django_db
def test_register_user_with_extra_fields(client):
    payload = {
        "email": "nuevo4@ejemplo.com",
        "password": "clave_segura123",
        "first_name": "Nuevo",
        "last_name": "Usuario",
        "extra_field": "valor",
    }
    response = client.post(reverse("users-list"), data=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == payload["email"]
    assert "extra_field" not in data


@pytest.mark.django_db
def test_register_user_empty_names(client):
    payload = {
        "email": "nuevo5@ejemplo.com",
        "password": "clave_segura123",
        "first_name": "",
        "last_name": "",
    }
    response = client.post(reverse("users-list"), data=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == payload["email"]
