from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    """
    מאפשר גישה לקריאה לכל אחד.
    עבור פעולות כתיבה (יצירה, עדכון, מחיקה):
      - מותרות אם המשתמש הוא סופר-משתמש או בעל הרשאת מנהל (is_staff),
        או אם המשתמש שייך לאחת הקבוצות "Editor", "Manager", "Admin",
        או שהוא המחבר של הכתבה (במקרה של עדכון/מחיקה).
    """
    def has_permission(self, request, view):
        # מתירים קריאה לכל אחד
        if request.method in SAFE_METHODS:
            return True

        # חובה שהמשתמש יהיה מאומת
        if not request.user or not request.user.is_authenticated:
            return False

        # אם המשתמש הוא סופר-משתמש או בעל הרשאת מנהל – מורשה
        if request.user.is_superuser or request.user.is_staff:
            return True

        # עבור יצירה – בדיקה לפי קבוצות אם נדרש
        return request.user.groups.filter(name__in=["Editor", "Manager", "Admin"]).exists()

    def has_object_permission(self, request, view, obj):
        # מתירים קריאה לכל אחד
        if request.method in SAFE_METHODS:
            return True

        # אם המשתמש הוא סופר-משתמש או בעל הרשאת מנהל – מורשה
        if request.user.is_superuser or request.user.is_staff:
            return True

        # אם המשתמש שייך לאחת הקבוצות – מורשה
        if request.user.groups.filter(name__in=["Editor", "Manager", "Admin"]).exists():
            return True

        # לבסוף, אם המשתמש הוא המחבר של הכתבה
        return obj.author == request.user
