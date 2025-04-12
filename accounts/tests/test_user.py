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
