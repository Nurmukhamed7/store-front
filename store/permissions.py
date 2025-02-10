from rest_framework import permissions

# Class look like IsAuthenticated
class isAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        # Разрешает изменения только админу
        return bool(request.user and request.user.is_staff)

# Авторизация (Authorization) – проверяет, имеешь ли ты права для выполнения действия
class FullDjangoModelPermissions(permissions.DjangoModelPermissions):
    def __init__(self):
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']
