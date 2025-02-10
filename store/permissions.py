from rest_framework import permissions

# Class look like IsAuthenticated
class isAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        # Разрешает изменения только админу
        return bool(request.user and request.user.is_staff)