from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from django.contrib.auth import authenticate, login, get_user_model
from rest_framework import generics
from django.contrib.auth import logout
from .models import User
from .serializers import UserRegistrationSerializer, UserSerializer, PasswordSerializer, LoginSerializer


class UserRegistrationView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = []
    authentication_classes = []
    serializer_class = UserRegistrationSerializer


class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        # Получение данных из тела запроса
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        username: str = serializer.validated_data.get('username')
        password: str = serializer.validated_data.get('password')

        # Аутентификация пользователя
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_active:
            # Успешная аутентификация и вход
            login(request, user)
            # Возвращаем данные пользователя в ответе
            response_data: dict = {
                'id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'provider': user.provider.id if user.provider else None
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            # Неуспешная аутентификация
            response_data: dict = {'error': 'Invalid username or password or user is inactive'}
            return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)


class UserProfileView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = []
    authentication_classes = []

    def get_object(self):
        return self.request.user

    def destroy(self, request, *args, **kwargs):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UpdatePasswordView(generics.UpdateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = PasswordSerializer
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = []
    authentication_classes = []

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        old_password: str = request.data.get('old_password')
        new_password: str = request.data.get('new_password')

        if not user.check_password(old_password):
            return Response({"error": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_password(new_password, user)
        except ValidationError as e:
            return Response({"error": e.messages}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({"success": "Password updated successfully"}, status=status.HTTP_200_OK)
