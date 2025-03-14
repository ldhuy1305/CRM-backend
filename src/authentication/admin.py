from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "email",
        "first_name",
        "last_name",
        "phone",
        "address",
    ]
    search_fields = ["first_name", "last_name", "email"]
