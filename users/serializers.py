from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from network.models import Provider
from network.serializers import ProviderSerializer
from .models import User


# class UserRegistrationSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
#     password_repeat = serializers.CharField(write_only=True, required=True)
#
#     class Meta:
#         model = User
#         fields = ('username', 'password', 'password_repeat', 'email', 'first_name', 'last_name')
#
#     def validate(self, attrs):
#         if attrs['password'] != attrs['password_repeat']:
#             raise serializers.ValidationError({"password_repeat": "Пароли не совпадают."})
#         return attrs
#
#     def create(self, validated_data):
#         user = User.objects.create(
#             username=validated_data['username'],
#             email=validated_data['email'],
#             first_name=validated_data['first_name'],
#             last_name=validated_data['last_name'],
#             provider=validated_data['provider']
#         )
#
#         user.set_password(validated_data['password'])
#         user.save()
#
#         return user

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_repeat = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password_repeat', 'email', 'first_name', 'last_name')
        extra_kwargs = {'provider': {'required': False}}

    def validate(self, attrs):
        if attrs['password'] != attrs['password_repeat']:
            raise serializers.ValidationError({"password_repeat": "Пароли не совпадают."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


# class ProviderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Provider
#         fields = '__all__'  # или перечислите поля, которые вы хотите включить


class UserSerializer(serializers.ModelSerializer):
    provider = ProviderSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'provider')
        read_only_fields = ('id',)


class PasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
