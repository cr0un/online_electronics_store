from django.urls import path
from users import views
from users.views import LoginView, UpdatePasswordView

app_name = 'users'

urlpatterns = [
    path('signup', views.UserRegistrationView.as_view(), name='signup'),
    path('login', LoginView.as_view(), name='login'),
    path('profile', views.UserProfileView.as_view(), name='profile'),
    path('update_password', UpdatePasswordView.as_view(), name='update_password'),
]
