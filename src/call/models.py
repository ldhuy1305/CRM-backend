# Create your models here.
from django.db import models

from account.models import Account
from authentication.models import User
from common.models import BaseModel, BaseNameModel
from contact.models import Contact
from deal.models import Deal
from lead.models import Lead


class CallPurpose(BaseNameModel):
    class Meta:
        ordering = ["-id"]
        db_table = "call_purpose"


class CallResult(BaseNameModel):
    class Meta:
        ordering = ["-id"]
        db_table = "call_result"


class CallType(BaseNameModel):
    class Meta:
        ordering = ["-id"]
        db_table = "call_type"


class Call(BaseModel):
    call_owner = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="calls"
    )
    call_purpose = models.ForeignKey(
        CallPurpose,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="calls",
    )
    call_result = models.ForeignKey(
        CallResult,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="calls",
    )
    call_type = models.ForeignKey(
        CallType, on_delete=models.SET_NULL, null=True, blank=True, related_name="calls"
    )

    lead = models.ForeignKey(
        Lead, on_delete=models.SET_NULL, null=True, blank=True, related_name="calls"
    )
    contact = models.ForeignKey(
        Contact, on_delete=models.SET_NULL, null=True, blank=True, related_name="calls"
    )
    related_account = models.ForeignKey(
        Account, on_delete=models.SET_NULL, null=True, blank=True, related_name="calls"
    )
    related_deal = models.ForeignKey(
        Deal, on_delete=models.SET_NULL, null=True, blank=True, related_name="calls"
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField()
    duration = models.IntegerField()

    class Meta:
        ordering = ["-id"]
        db_table = "call"
        app_label = "call"
