from rest_framework import serializers
from .models import Provider, Product, Contact


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = '__all__'
        read_only_fields = ('debt', 'level', 'created_at', 'updated_at')

    contact = ContactSerializer()
    products = ProductSerializer(many=True, read_only=True)
