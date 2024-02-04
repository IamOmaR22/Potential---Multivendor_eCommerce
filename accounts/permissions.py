from rest_framework import permissions

class IsAccountType(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False

        # Check if the user's user_type is allowed for this view
        allowed_roles = getattr(view, 'allowed_roles', None)

        if allowed_roles is None:
            return True  # No specific role required for this view

        return request.user.user_type in allowed_roles