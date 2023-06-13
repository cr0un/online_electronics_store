from factory import Faker, fuzzy
from factory.django import DjangoModelFactory
from datetime import datetime
from users.models import User
from network.models import Product, Provider


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = Faker("first_name")
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    email = Faker("safe_email")
    password = Faker("password")

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        return cls._get_manager(model_class).create_user(*args, **kwargs)


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    title = Faker("name")
    model = Faker("name")
    date_release = fuzzy.FuzzyNaiveDateTime(datetime(2023, 1, 1))


class ProviderFactory(DjangoModelFactory):
    class Meta:
        model = Provider

    type = fuzzy.FuzzyInteger(0, 3)
    title = Faker("name")
    email = Faker("email")
    country = Faker("country")
    city = Faker("city")
    street = Faker("name")
    house = Faker("name")
