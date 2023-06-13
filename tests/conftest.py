from pytest_factoryboy import register

from tests.factories import UserFactory, ProductFactory, ProviderFactory


register(UserFactory)
register(ProductFactory)
register(ProviderFactory)

pytest_plugins = 'tests.fixtures'
