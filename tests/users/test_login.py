import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestLogin:
    url = reverse('users:login')

    def test_login_successfull(self, client, user_factory, faker):
        password = faker.password()
        user = user_factory.create(password=password)
        response = client.post(self.url, data={
            'username': user.username,
            'password': password,
        })
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {'username': user.username, 'password': password}

    def test_login_user_not_found(self, client, user_factory, faker):
        user = user_factory.build()
        response = client.post(self.url, data={
            'username': user.username,
            'password': faker.password(),
        })
        assert response.status_code == status.HTTP_403_FORBIDDEN
