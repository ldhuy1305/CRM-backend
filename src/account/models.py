from django.db import models

from api import settings
from authentication.models import User
from common.models import BaseModel, BaseNameModel
from lead.models import Industry, Lead


class AccountType(BaseNameModel):
    class Meta:
        ordering = ["-id"]
        db_table = "account_type"


class Rating(BaseNameModel):
    class Meta:
        ordering = ["-id"]
        db_table = "rating"


class Account(BaseModel):
    account_owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="owned_account",
    )
    account_type = models.ForeignKey(
        AccountType, on_delete=models.SET_NULL, null=True, blank=True
    )
    convert_from = models.ForeignKey(
        Lead,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="converted_account",
    )
    industry = models.ForeignKey(
        Industry,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="account",
    )
    rating = models.ForeignKey(Rating, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True, null=True)
    fax = models.CharField(max_length=20, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    tax_code = models.CharField(max_length=50, blank=True, null=True)
    employees = models.PositiveIntegerField(blank=True, null=True)
    avatar = models.URLField(blank=True, null=True, default=settings.DEFAULT_AVATAR)
    annual_revenue = models.DecimalField(
        max_digits=15, decimal_places=2, blank=True, null=True
    )

    street = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state_province = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)

    description = models.TextField(blank=True, null=True)

    SEARCH_FIELDS_CONTAINS = dict(
        name="name",
        website="website",
        phone="phone",
    )

    SEARCH_FIELDS = dict(
        account_owner="account_owner",
    )
    EXCEL_HEADERS = [
        ("name", "Account Name"),
        ("phone", "Phone"),
        ("website", "Website"),
        ("phone", "Phone"),
        ("industry.name", "Industry"),
        ("account_owner.full_name", "Owner"),
    ]

    class Meta:
        ordering = ["-id"]
        db_table = "account"
        app_label = "account"
