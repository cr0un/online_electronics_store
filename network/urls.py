from django.urls import path
from .views import ProviderListView, ProviderCreateView, ProviderView, ProductListView, ProductCreateView, ProductView

urlpatterns = [
    path('product/list', ProductListView.as_view(), name='product_list'),
    path('product/create', ProductCreateView.as_view(), name='product_create_view'),
    path('product/<pk>', ProductView.as_view(), name='product_view'),

    path('provider/list', ProviderListView.as_view(), name='provider_list'),
    path('provider/create', ProviderCreateView.as_view(), name='provider_create_view'),
    path('provider/<pk>', ProviderView.as_view(), name='provider_view'),
]
