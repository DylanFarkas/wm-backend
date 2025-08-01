from rest_framework.permissions import BasePermission

class IsAppAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and getattr(request.user, 'role', '') == 'admin'
