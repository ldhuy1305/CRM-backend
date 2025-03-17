from rest_framework.permissions import BasePermission

from api.constants import GroupNameEnum


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if not bool(request.user and request.user.is_authenticated):
            return False

        return True


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.groups.filter(name=GroupNameEnum.ADMIN.value).exists():
            return True

        return False


class IsManager(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.groups.filter(name=GroupNameEnum.MANGER.value).exists():
            return True

        return False


class IsSalesman(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.groups.filter(name=GroupNameEnum.SALESMAN.value).exists():
            return True

        return False


class IsMarketer(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.groups.filter(name=GroupNameEnum.MARKETER.value).exists():
            return True

        return False
