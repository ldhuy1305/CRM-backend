from django.db import models

from api.common import BaseModel
from campaign.models import Campaign
from contact.models import Contact
from lead.models import Lead

# Create your models here.


class CampaignTarget(BaseModel):
    campaign = models.ForeignKey(
        Campaign, on_delete=models.SET_NULL, null=True, related_name="campaign_targets"
    )
    lead = models.ForeignKey(
        Lead, on_delete=models.SET_NULL, null=True, related_name="campaign_targets"
    )
    contact = models.ForeignKey(
        Contact, on_delete=models.SET_NULL, null=True, related_name="campaign_targets"
    )

    class Meta:
        ordering = ["-id"]
        db_table = "campaign_target"
        app_label = "campaign_target"
