from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsITStaffOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        user = request.user
        profile = getattr(user, "profile", None)
        is_it_staff = getattr(profile, "is_it_staff", False)

        if is_it_staff:
            return True
        return False
