from rest_framework.permissions import BasePermission

from api.constants import UserRoleEnum

class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        print(request.user)
        if not bool(
                request.user and request.user.is_authenticated
        ):
            return False

        return True
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if not bool(
                request.user and request.user.is_authenticated and request.user.role_id == UserRoleEnum.ADMIN.value
        ):
            return False

        return True

class IsSales(BasePermission):
    def has_permission(self, request, view):
        if not bool(
                request.user and request.user.is_authenticated and request.user.role_id == UserRoleEnum.SALES.value
        ):
            return False

        return True

class IsMarketing(BasePermission):
    def has_permission(self, request, view):
        if not bool(
                request.user and request.user.is_authenticated and request.user.role_id == UserRoleEnum.MARKETING.value
        ):
            return False

        return True
