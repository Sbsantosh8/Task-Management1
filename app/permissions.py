from rest_framework.permissions import BasePermission


class IsAdminOrManager(BasePermission):
    """Permission for Admins and Managers to manage tasks."""

    # def has_permission(self, request, view):
    #     return request.user.is_authenticated and request.user.role in [
    #         "admin",
    #         "manager",
    #     ]

    def has_permission(self, request, view):
        print(f"Authenticated: {request.user.is_authenticated}")
        print(f"User: {request.user}")
        print(f"Role: {getattr(request.user, 'role', None)}")

        return request.user.is_authenticated and getattr(
            request.user, "role", None
        ) in ["admin", "manager"]


from rest_framework.permissions import BasePermission


class IsTaskOwnerOrManager(BasePermission):
    """Allows Employees to view their assigned tasks & Managers to see all tasks."""

    def has_permission(self, request, view):
        return request.user.is_authenticated  # Allow all authenticated users

    def has_object_permission(self, request, view, obj):
        return request.user.role == "manager" or obj.assigned_to == request.user
