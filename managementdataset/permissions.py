# permissions.py

from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated and is an admin
        return request.user and request.user.is_staff