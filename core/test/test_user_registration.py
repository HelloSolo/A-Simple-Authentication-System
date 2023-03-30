import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.core import mail


@pytest.mark.django_db
class TestUserRegistration:
    def test_user_registion_valid_data(self, api_client):
        response = api_client.post(
            "/auth/users/",
            {
                "email": "test_user@domain.com",
                "first_name": "Test",
                "last_name": "User",
                "password": "qpdkri1230",
            },
        )

        assert response.status_code == status.HTTP_201_CREATED

    def test_user_registration_invalid_password(self):
        client = APIClient()
        response = client.post(
            "/auth/users/",
            {
                "email": "test_user@domain.com",
                "first_name": "Test",
                "last_name": "User",
                "password": "",
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_user_registration_invalid_email(self):
        client = APIClient()
        response = client.post(
            "/auth/users/",
            {
                "email": "",
                "first_name": "Test",
                "last_name": "User",
                "password": "qpdkri1230",
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_activation_email_is_sent(self):
        client = APIClient()
        response = client.post(
            "/auth/users/",
            {
                "email": "test_user@domain.com",
                "first_name": "Test",
                "last_name": "User",
                "password": "qpdkri1230",
            },
        )

        assert len(mail.outbox) == 1

    def test_activation_link_in_email(self):
        user = {
            "email": "test_user@domain.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "qpdkri1230",
        }

        client = APIClient()
        client.post(
            "/auth/users/",
            user,
        )
        uid, token = [l for l in mail.outbox[0].body.splitlines() if "/activate/" in l][
            0
        ].split("/")[-2:]
        response = client.post("/auth/users/activation/", {"uid": uid, "token": token})

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_activation_link_with_invalid_token_uid(self):
        client = APIClient()
        response = client.post("/auth/users/activation/", {"uid": "", "token": ""})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_resend_activation_email(self):
        user = {
            "email": "test_user@domain.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "qpdkri1230",
        }

        client = APIClient()
        client.post(
            "/auth/users/",
            user,
        )
