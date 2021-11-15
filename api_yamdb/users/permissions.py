from rest_framework import permissions, status
from email_jwt_auth.exceptions import CustomValidation


class IsAdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (request.user.is_admin or request.user.is_superuser)
        raise CustomValidation("Вы не авторизованы!", "Autorization",
                               status_code=status.HTTP_401_UNAUTHORIZED)

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (request.user.is_admin or request.user.is_superuser)
        return False


class IsOwnerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        raise CustomValidation("Вы не авторизованы!", "Autorization",
                               status_code=status.HTTP_401_UNAUTHORIZED)

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return request.user == obj
        return False
