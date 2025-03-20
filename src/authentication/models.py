# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

from api import settings
from common.models import TimestampedModel

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin, TimestampedModel):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True, db_index=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    avatar = models.URLField(blank=True, null=True, default=settings.DEFAULT_AVATAR)
    is_verified = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email

        super().save(*args, **kwargs)

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        refresh["username"] = self.username
        refresh["email"] = self.email

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    def get_full_name(self):
        try:
            full_name = f"{self.last_name} {self.first_name}"
        except AttributeError:
            full_name = self.email
        return full_name.strip()

    class Meta:
        ordering = ["-id"]
        db_table = "user"


class UserVerifyCode(TimestampedModel):
    id = models.BigAutoField(primary_key=True)
    code = models.CharField(max_length=8)
    expired_at = models.DateTimeField()
    verify_time = models.IntegerField(default=0)
    user = models.ForeignKey(
        "User", to_field="id", related_name="user_verify_code", on_delete=models.CASCADE
    )

    class Meta:
        db_table = "user_verify_code"
