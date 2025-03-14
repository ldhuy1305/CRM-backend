from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create group for super admin"

    def handle(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name="Super Admin")
        permissions = Permission.objects.all()
        group.permissions.set(permissions)
