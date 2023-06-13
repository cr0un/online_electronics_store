from rest_framework import permissions


class IsActiveUser(permissions.BasePermission):
    """Настройка доступа активным пользователям"""
    def has_permission(self, request, view):
        if request.user.is_active:
            return True
        return False
