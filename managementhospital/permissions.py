# permissions.py

from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        # Solo usuarios administradores pueden acceder
        return request.user and request.user.is_staff