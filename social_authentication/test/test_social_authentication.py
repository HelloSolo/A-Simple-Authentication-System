import pytest
from rest_framework import status


@pytest.mark.db_django
class TestSocialAuthentication:
    def test_social_auth_with_valid_auth_token(self, api_client):
        auth_token = ""

        response = api_client.post("/auth/social/google/", auth_token)

        assert response.status_code == status.HTTP_201_CREATED
