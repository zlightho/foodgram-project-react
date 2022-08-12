from rest_framework.permissions import SAFE_METHODS, BasePermission


class RecipePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user == obj.author
            or request.user.is_superuser
            or request.method in SAFE_METHODS
        )
