from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from network.models import Provider


class User(AbstractUser):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, null=True, blank=True, related_name='users')

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username
