# Create your models here.
from django.db import models

from account.models import Account
from api import settings
from authentication.models import User
from lead.models import LeadSource


class Contact(models.Model):
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

    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    department = models.CharField(max_length=255, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)

    assistant_name = models.CharField(max_length=255, null=True, blank=True)
    assistant_phone = models.CharField(max_length=20, null=True, blank=True)
    avatar = models.URLField(blank=True, null=True, default=settings.DEFAULT_AVATAR)

    is_email_opt_out = models.BooleanField(default=False)
    is_call_opt_out = models.BooleanField(default=False)

    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["-id"]
        db_table = "contact"
