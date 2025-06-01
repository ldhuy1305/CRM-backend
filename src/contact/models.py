# Create your models here.
from django.db import models

from account.models import Account
from api import settings
from authentication.models import User
from common.models import BaseModel
from lead.models import LeadSource


class Contact(BaseModel):
    contact_owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="owned_contacts",
    )
    lead_source = models.ForeignKey(
        LeadSource,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="contacts",
    )
    account = models.ForeignKey(
        Account,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="contacts",
    )

    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    fax = models.CharField(max_length=20, null=True, blank=True)
    department = models.CharField(max_length=255, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)

    assistant_name = models.CharField(max_length=255, null=True, blank=True)
    assistant_phone = models.CharField(max_length=20, null=True, blank=True)
    avatar = models.URLField(blank=True, null=True, default=settings.DEFAULT_AVATAR)

    is_email_opt_out = models.BooleanField(default=False)
    is_call_opt_out = models.BooleanField(default=False)

    street = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state_province = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)

    description = models.TextField(blank=True, null=True)

    SEARCH_FIELDS_CONTAINS = dict(
        first_name="first_name",
        company="company_name",
        email="email",
        phone="phone",
    )

    SEARCH_FIELDS = dict(
        account="account",
        contact_owner="contact_owner",
    )

    class Meta:
        ordering = ["-id"]
        db_table = "contact"

    @property
    def full_name(self):
        try:
            full_name = f"{self.last_name} {self.first_name}"
        except AttributeError:
            full_name = self.email
        return full_name.strip()
