from rest_framework import permissions
from users.constants import ADMIN, MODERATOR


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Доступ на изменение авторам, остальным на чтение.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsModerator(permissions.BasePermission):
    """
    Доступ пользователям с ролью moderator.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == MODERATOR
        )


class IsAdmin(permissions.BasePermission):
    """
    Доступ пользователям с ролью admin или superuser.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (
                request.user.is_superuser
                or request.user.role == ADMIN
            )
        )
