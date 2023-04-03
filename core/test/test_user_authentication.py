import pytest
from rest_framework import status
from django.core import mail


@pytest.fixture
def login_user(api_client):
    def do_login_user(data={"email": "test_user@domain.com", "password": "qpdkri1230"}):
        return api_client.post("/auth/jwt/create", data)

    return do_login_user


@pytest.mark.django_db
class TestUserLogin:
    def test_user_login_with_valid_credentials(
        self, api_client, create_user, login_user
    ):
        create_user()
        uid, token = [l for l in mail.outbox[0].body.splitlines() if "/activate/" in l][
            0
        ].split("/")[-2:]
        api_client.post("/auth/users/activation/", {"uid": uid, "token": token})
        response = login_user()

        assert response.status_code == status.HTTP_200_OK
        assert "access" and "refresh" in response.data

    def test_login_with_unregistered_user(self, login_user):
        response = login_user(
            {"email": "test_user@domain.com", "password": "qpdkri1230"}
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_with_unactivated_account(self, create_user, login_user):
        create_user()
        response = login_user()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
