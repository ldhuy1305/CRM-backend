from django.db import models

from account.models import Account
from authentication.models import User
from campaign.models import Campaign
from common.models import BaseModel
from contact.models import Contact
from deal.models import Deal
from lead.models import Lead


# Create your models here.
class Note(BaseModel):
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="notes_created_by"
    )
    lead = models.ForeignKey(
        Lead, on_delete=models.SET_NULL, null=True, blank=True, related_name="notes"
    )
    contact = models.ForeignKey(
        Contact, on_delete=models.SET_NULL, null=True, blank=True, related_name="notes"
    )
    account = models.ForeignKey(
        Account, on_delete=models.SET_NULL, null=True, blank=True, related_name="notes"
    )
    deal = models.ForeignKey(
        Deal, on_delete=models.SET_NULL, null=True, blank=True, related_name="notes"
    )
    campaign = models.ForeignKey(
        Campaign, on_delete=models.SET_NULL, null=True, blank=True, related_name="notes"
    )
    note_body = models.TextField()

    class Meta:
        ordering = ["-id"]
        db_table = "note"
        app_label = "note"
