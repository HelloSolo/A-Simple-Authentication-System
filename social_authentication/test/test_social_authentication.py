import pytest
import os
from dotenv import load_dotenv
from django.conf import settings
from rest_framework import status


@pytest.fixture
def get_google_token(api_client):
    def do_get_token(credential):
        return api_client.post("/auth/social/google/", {"credential": credential})

    return do_get_token


@pytest.fixture
def get_facebook_token(api_client):
    def do_get_token(credential):
        return api_client.post("/auth/social/facebook/", {"credential": credential})

    return do_get_token


@pytest.mark.django_db
class TestGoogleSocialAuthentication:
    def test_social_auth_with_valid_credential(self, get_google_token):
        credential = settings.GOOGLE_CREDENTIAL

        response = get_google_token(credential)

        assert response.status_code == status.HTTP_200_OK

    def test_social_auth_with_invalid_credential(self, get_google_token):
        credential = os.environ.get("INVALID_TOKEN")

        response = get_google_token(credential)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_social_with_illegally_generated_credential(self, get_google_token):
        credential = os.environ.get("ILLEGAL_TOKEN")

        response = get_google_token(credential)

        assert response.status_code == (status.HTTP_401_UNAUTHORIZED)


@pytest.mark.django_db
class TestFacebookSocialAuthentication:
    @pytest.mark.skip
    def test_social_auth_with_valid_credential(self, get_facebook_token):
        credential = settings.FACEBOOK_CREDENTIAL

        response = get_facebook_token(credential)

        assert response.status_code == status.HTTP_200_OK

    def test_social_auth_with_invalid_credential(self, get_facebook_token):
        credential = os.environ.get("INVALID_TOKEN")

        response = get_facebook_token(credential)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
