import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def activate_user(api_client, create_user):
    def do_activate_user(data):
        create_user()

        return api_client.post("/auth/users/activation/", data)

    return do_activate_user
