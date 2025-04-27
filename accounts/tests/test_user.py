import pytest
from django.urls import reverse
from rest_framework import status

from accounts.factories import UserFactory


@pytest.mark.django_db
def test_login(client):
    user = UserFactory()
    payload = {
        "email": user.email,
        "password": "secretpassword",
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
    payload = {
        "email": "noexiste@ejemplo.com",
        "password": "secretpassword",
    }
    response = client.post(reverse("token_obtain_pair"), data=payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    data = response.json()
    assert "access" not in data and "refresh" not in data


@pytest.mark.django_db
def test_login_wrong_password(client):
    user = UserFactory()
    payload = {
        "email": user.email,
        "password": "incorrecta",
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
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


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
        "income": "100000.00",
        "partner_first_name": "Pareja",
        "partner_last_name": "Apellido",
        "partner_email": "pareja@ejemplo.com",
        "partner_income": "80000.00",
    }
    response = client.post(reverse("users-list"), data=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == payload["email"]
    assert data["first_name"] == payload["first_name"]
    assert data["last_name"] == payload["last_name"]
    assert "password" not in data

    # Check both users exist
    from accounts.models import User
    from expenses.models.group import Group, GroupMember

    user = User.objects.get(email=payload["email"])
    partner = User.objects.get(email=payload["partner_email"])
    assert user.is_active is True
    assert partner.is_active is False

    # Check group and group members
    group = Group.objects.filter(members__user=user).first()
    assert group is not None
    members = GroupMember.objects.filter(group=group)
    assert members.count() == 2
    main_member = members.get(user=user)
    partner_member = members.get(user=partner)
    assert main_member.income == float(payload["income"])
    assert main_member.role == GroupMember.ADMIN
    assert partner_member.income == float(payload["partner_income"])
    assert partner_member.role == GroupMember.MEMBER
    assert main_member.income_currency == "ARS"
    assert partner_member.income_currency == "ARS"
    assert main_member.income_frequency == GroupMember.MONTHLY
    assert partner_member.income_frequency == GroupMember.MONTHLY


@pytest.mark.django_db
def test_register_user_missing_required_fields(client):
    """
    Test registration fails if any required field is missing.
    Should return 400 and specify the missing field(s).
    """
    required_fields = [
        "email",
        "password",
        "income",
        "first_name",
        "last_name",
        "partner_first_name",
        "partner_last_name",
        "partner_email",
        "partner_income",
    ]
    base_payload = {
        "email": "nuevo@ejemplo.com",
        "password": "clave_segura123",
        "first_name": "Nuevo",
        "last_name": "Usuario",
        "income": "100000.00",
        "partner_first_name": "Pareja",
        "partner_last_name": "Apellido",
        "partner_email": "parejamissing@ejemplo.com",
        "partner_income": "80000.00",
    }
    for field in required_fields:
        payload = base_payload.copy()
        payload.pop(field)
        response = client.post(reverse("users-list"), data=payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        data = response.json()
        assert field in data


@pytest.mark.django_db
def test_register_user_duplicate_email(client):
    """
    Test registration fails if the main user's email already exists.
    Should return 400 and specify the email field.
    """
    from accounts.factories import UserFactory

    UserFactory(email="nuevo@ejemplo.com")
    payload = {
        "email": "nuevo@ejemplo.com",
        "password": "clave_segura123",
        "first_name": "Nuevo",
        "last_name": "Usuario",
        "income": "100000.00",
        "partner_first_name": "Pareja",
        "partner_last_name": "Apellido",
        "partner_email": "parejadup@ejemplo.com",
        "partner_income": "80000.00",
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
    """
    Test registration fails if password is empty.
    Should return 400 and specify the password field.
    """
    payload = {
        "email": "nuevo3@ejemplo.com",
        "password": "",
        "first_name": "Nuevo",
        "last_name": "Usuario",
        "income": "100000.00",
        "partner_first_name": "Pareja",
        "partner_last_name": "Apellido",
        "partner_email": "pareja3@ejemplo.com",
        "partner_income": "80000.00",
    }
    response = client.post(reverse("users-list"), data=payload)
    assert response.status_code == 400
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
        "income": "100000.00",
        "partner_first_name": "Pareja",
        "partner_last_name": "Apellido",
        "partner_email": "parejaextra@ejemplo.com",
        "partner_income": "80000.00",
        "extra_field": "valor",
    }
    response = client.post(reverse("users-list"), data=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == payload["email"]
    assert "extra_field" not in data


@pytest.mark.django_db
def test_register_user_partner_email_duplicate(client):
    from accounts.factories import UserFactory

    UserFactory(email="pareja@ejemplo.com")
    payload = {
        "email": "nuevo2@ejemplo.com",
        "password": "clave_segura123",
        "first_name": "Nuevo",
        "last_name": "Usuario",
        "income": "100000.00",
        "partner_first_name": "Pareja",
        "partner_last_name": "Apellido",
        "partner_email": "pareja@ejemplo.com",
        "partner_income": "80000.00",
    }
    response = client.post(reverse("users-list"), data=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    data = response.json()
    assert "partner_email" in data


@pytest.mark.django_db
def test_register_user_negative_income(client):
    """
    Test registration fails if income or partner_income is negative.
    Should return 400 and specify the invalid field(s).
    """
    payload = {
        "email": "nuevo4@ejemplo.com",
        "password": "clave_segura123",
        "first_name": "Nuevo",
        "last_name": "Usuario",
        "income": "-1000.00",
        "partner_first_name": "Pareja",
        "partner_last_name": "Apellido",
        "partner_email": "parejaneg@ejemplo.com",
        "partner_income": "80000.00",
    }
    response = client.post(reverse("users-list"), data=payload)
    assert response.status_code == 400
    data = response.json()
    assert "income" in data

    payload["income"] = "100000.00"
    payload["partner_income"] = "-500.00"
    response = client.post(reverse("users-list"), data=payload)
    assert response.status_code == 400
    data = response.json()
    assert "partner_income" in data


@pytest.mark.django_db
def test_register_user_duplicate_partner_email(client):
    """
    Test registration fails if the partner's email already exists.
    Should return 400 and specify the partner_email field.
    """
    from accounts.factories import UserFactory

    UserFactory(email="parejadup@ejemplo.com")
    payload = {
        "email": "nuevo2@ejemplo.com",
        "password": "clave_segura123",
        "first_name": "Nuevo",
        "last_name": "Usuario",
        "income": "100000.00",
        "partner_first_name": "Pareja",
        "partner_last_name": "Apellido",
        "partner_email": "parejadup@ejemplo.com",
        "partner_income": "80000.00",
    }
    response = client.post(reverse("users-list"), data=payload)
    assert response.status_code == 400
    data = response.json()
    assert "partner_email" in data


@pytest.mark.django_db
def test_register_user_invalid_email_format(client):
    """
    Test registration fails if email or partner_email is not a valid email.
    Should return 400 and specify the invalid field(s).
    """
    payload = {
        "email": "notanemail",
        "password": "clave_segura123",
        "first_name": "Nuevo",
        "last_name": "Usuario",
        "income": "100000.00",
        "partner_first_name": "Pareja",
        "partner_last_name": "Apellido",
        "partner_email": "pareja@ejemplo.com",
        "partner_income": "80000.00",
    }
    response = client.post(reverse("users-list"), data=payload)
    assert response.status_code == 400
    data = response.json()
    assert "email" in data

    payload["email"] = "nuevo@ejemplo.com"
    payload["partner_email"] = "notanemail"
    response = client.post(reverse("users-list"), data=payload)
    assert response.status_code == 400
    data = response.json()
    assert "partner_email" in data


@pytest.mark.django_db
def test_register_user_extra_fields_ignored(client):
    """
    Test registration ignores extra fields not defined in the serializer.
    Should return 201 and not include the extra field in the response.
    """
    payload = {
        "email": "nuevo6@ejemplo.com",
        "password": "clave_segura123",
        "first_name": "Nuevo",
        "last_name": "Usuario",
        "income": "100000.00",
        "partner_first_name": "Pareja",
        "partner_last_name": "Apellido",
        "partner_email": "parejaextra@ejemplo.com",
        "partner_income": "80000.00",
        "extra_field": "valor",
    }
    response = client.post(reverse("users-list"), data=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == payload["email"]
    assert "extra_field" not in data


@pytest.mark.django_db
def test_register_user_empty_names(client):
    """
    Test registration fails if first_name, last_name,
    partner_first_name, or partner_last_name are empty.
    Should return 400 and specify the invalid field(s).
    """
    payload = {
        "email": "nuevo5@ejemplo.com",
        "password": "clave_segura123",
        "first_name": "",
        "last_name": "",
        "income": "100000.00",
        "partner_first_name": "",
        "partner_last_name": "",
        "partner_email": "parejavacia@ejemplo.com",
        "partner_income": "80000.00",
    }
    response = client.post(reverse("users-list"), data=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    data = response.json()
    assert "first_name" in data
    assert "last_name" in data
    assert "partner_first_name" in data
    assert "partner_last_name" in data
