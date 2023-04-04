import pytest
from rest_framework import status
from django.core import mail


@pytest.fixture
def activate_user(api_client, create_user):
    def do_activate_user(data):
        create_user()

        return api_client.post("/auth/users/activation/", data)

    return do_activate_user


@pytest.mark.django_db
class TestUserRegistration:
    def test_user_registion_valid_data(self, create_user):
        response = create_user()

        assert response.status_code == status.HTTP_201_CREATED

    def test_user_registration_invalid_password(self, create_user):
        response = create_user(
            {
                "email": "test_user@domain.com",
                "first_name": "Test",
                "last_name": "User",
                "password": "",
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_user_registration_invalid_email(self, create_user):
        response = create_user(
            {
                "email": "",
                "first_name": "Test",
                "last_name": "User",
                "password": "qpdkri1230",
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_activation_email_is_sent(self, create_user):
        create_user()

        assert len(mail.outbox) == 1

    def test_activation_link_in_email(self, create_user, activate_user):
        create_user()
        uid, token = [l for l in mail.outbox[0].body.splitlines() if "/activate/" in l][
            0
        ].split("/")[-2:]
        response = activate_user({"uid": uid, "token": token})

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_activation_link_with_invalid_token_uid(self, activate_user):
        response = activate_user({"uid": "", "token": ""})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_resend_activation_email(self, api_client, create_user):
        create_user()
        api_client.post(
            "/auth/users/resend_activation/", {"email": "test_user@domain.com"}
        )
        assert len(mail.outbox) == 2  # one for email activation, the other for resend
