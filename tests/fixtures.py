import pytest
from rest_framework.test import APIClient


@pytest.fixture
def client() -> APIClient:
    return APIClient()


@pytest.fixture
@pytest.mark.django_db
def auth_client(client, user) -> APIClient:
    client.force_login(user)
    return client