import pytest
from django.urls import reverse
from rest_framework import status

from tests.factories import UserFactory


@pytest.mark.django_db
class TestSignup:
    # url = reverse('users:signup')
    # def test_signup_success(self, client, user_factory):
    #     user_data = user_factory.build(
    #         first_name='First Name',
    #         last_name='Last Name',
    #         email='test@fdgdf.com',
    #     )
    #
    #     response = client.post(self.url, data={
    #         'username': user_data.username,
    #         'password': user_data.password,
    #         'password_repeat': user_data.password,
    #         'email': user_data.email,
    #         'first_name': user_data.first_name,
    #         'last_name': user_data.last_name,
    #     })
    #
    #     assert response.status_code == status.HTTP_201_CREATED

    def test_signup_success(self, client):
        user_data = {
            "username": "testuser",
            "password": "Mm_123456",
            "password_repeat": "Mm_123456",
            "email": "test@fdgdf.com",
            "first_name": "First Name",
            "last_name": "Last Name",
        }
        url = reverse('users:signup')
        response = client.post(url, user_data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_signup_invalid_password(self, client):
        user_data = {
            "username": "testuser",
            "password": "Mm_123456",
            "password_repeat": "Mm_123456787787",
            "email": "test@fdgdf.com",
            "first_name": "First Name",
            "last_name": "Last Name",
        }
        url = reverse('users:signup')
        response = client.post(url, user_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
