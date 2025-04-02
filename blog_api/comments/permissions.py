from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrAdminOrReadOnly(BasePermission):
    """
    מאפשר גישה לקריאה לכל אחד.
    עבור יצירה (POST): כל משתמש מאומת רשאי.
    עבור עדכון/מחיקה: מורשה אם המשתמש הוא סופר-משתמש, מנהל (is_staff)
    או הבעלים של התגובה.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.method == "POST":
            return request.user and request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_superuser or request.user.is_staff:
            return True
        return obj.user == request.user
