# Create your models here.
from django.db import models

from authentication.models import User
from common.models import BaseModel, BaseNameModel, TimestampedModel
from contact.models import Contact


class CampaignType(BaseNameModel):
    class Meta:
        ordering = ["-id"]
        db_table = "campaign_type"


class CampaignStatus(BaseNameModel):
    class Meta:
        ordering = ["-id"]
        db_table = "campaign_status"


class Campaign(BaseModel):
    campaign_owner = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="campaign_owner"
    )
    campaign_type = models.ForeignKey(
        CampaignType, on_delete=models.SET_NULL, null=True
    )
    campaign_status = models.ForeignKey(
        CampaignStatus, on_delete=models.SET_NULL, null=True
    )

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    expected_revenue = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True
    )
    budgeted_cost = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True
    )
    actual_cost = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True
    )
    expected_response = models.FloatField(null=True, blank=True)
    numbers_sent = models.IntegerField(null=True, blank=True)

    SEARCH_FIELDS_CONTAINS = dict(
        name="name",
        company="company_name",
    )

    SEARCH_FIELDS = dict(
        type="campaign_type",
        status="campaign_status",
        start_date="start_date",
        end_date="end_date",
        campaign_owner="campaign_owner",
    )

    EXCEL_HEADERS = [
        ("name", "Campaign Name"),
        ("campaign_type.name", "Type"),
        ("start_date__date", "Start Date"),
        ("end_date__date", "End Date"),
        ("expected_revenue", "Expected Revenue"),
        ("actual_cost", "Actual Revenue"),
        ("campaign_owner.full_name", "Owner"),
    ]

    class Meta:
        ordering = ["-id"]
        db_table = "campaign"
        app_label = "campaign"
