from django.contrib import admin

from .models import Role, User


# Register your models here.
@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ["pk", "name"]
    search_fields = ["name"]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "pk",
        "email",
        "first_name",
        "last_name",
        "phone",
        "address",
        "role",
    ]
    search_fields = ["first_name", "last_name", "email"]