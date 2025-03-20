from django.db import models

from account.models import Account
from call.models import Call
from campaign.models import Campaign
from common.models import BaseModel, BaseNameModel
from contact.models import Contact
from deal.models import Deal
from lead.models import Lead
from meeting.models import Meeting
from task.models import Task


# Create your models here.
class Tag(BaseNameModel):
    class Meta:
        ordering = ["-id"]
        db_table = "tag"


class TagItems(BaseModel):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name="tag_items")
    lead = models.ForeignKey(
        Lead, on_delete=models.SET_NULL, null=True, blank=True, related_name="tag_items"
    )
    contact = models.ForeignKey(
        Contact,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tag_items",
    )
    account = models.ForeignKey(
        Account,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tag_items",
    )
    deal = models.ForeignKey(
        Deal, on_delete=models.SET_NULL, null=True, blank=True, related_name="tag_items"
    )
    task = models.ForeignKey(
        Task, on_delete=models.SET_NULL, null=True, blank=True, related_name="tag_items"
    )
    meeting = models.ForeignKey(
        Meeting,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tag_items",
    )
    call = models.ForeignKey(
        Call, on_delete=models.SET_NULL, null=True, blank=True, related_name="tag_items"
    )
    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tag_items",
    )

    class Meta:
        ordering = ["-id"]
        db_table = "tag_item"
        app_label = "tag_item"
