from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    """
    Allows read-only access to any request.
    For write operations:
        - Creation: Allowed only if the user is authenticated and belongs to one of the groups: "Editor", "Manager", or "Admin".
        - Update/Delete: Allowed if the user is superuser, belongs to one of the allowed groups,
                        or is the author of the article.
    """
    def has_permission(self, request, view):
        # Allow read-only methods for any request.
        if request.method in SAFE_METHODS:
            return True

        # Must be authenticated for write operations.
        if not request.user or not request.user.is_authenticated:
            return False

        # Superusers can do anything.
        if request.user.is_superuser:
            return True

        # For creation, allow only if user is in allowed groups.
        return request.user.groups.filter(name__in=["Editor", "Manager", "Admin"]).exists()

    def has_object_permission(self, request, view, obj):
        # Allow read-only methods.
        if request.method in SAFE_METHODS:
            return True

        # Superusers can update/delete anything.
        if request.user.is_superuser:
            return True

        # Allow update/delete if the user belongs to allowed groups.
        if request.user.groups.filter(name__in=["Editor", "Manager", "Admin"]).exists():
            return True

        # Otherwise, allow only if the user is the author of the article.
        return obj.author == request.user
