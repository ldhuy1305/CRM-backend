from django.db import models

from account.models import Account
from api.common import BaseModel, BaseNameModel, TimestampedModel
from authentication.models import User
from campaign.models import Campaign
from contact.models import Contact


# Create your models here.
class Stage(BaseNameModel):
    probability = models.FloatField()

    class Meta:
        ordering = ["-id"]
        db_table = "stage"


class LostReason(TimestampedModel):
    reason = models.CharField(max_length=500, unique=True)

    def __str__(self):
        return self.reason

    class Meta:
        ordering = ["-id"]
        db_table = "lost_reason"


class Deal(BaseModel):
    deal_owner = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="deal_owner"
    )
    account = models.ForeignKey(
        Account, on_delete=models.SET_NULL, null=True, related_name="account"
    )
    contact = models.ForeignKey(
        Contact, on_delete=models.SET_NULL, null=True, related_name="contact"
    )
    campaign = models.ForeignKey(
        Campaign, on_delete=models.SET_NULL, null=True, related_name="campaign"
    )
    lost_reason = models.ForeignKey(
        LostReason, on_delete=models.SET_NULL, null=True, blank=True
    )

    name = models.CharField(max_length=255)
    close_date = models.DateField(null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    probability = models.FloatField(default=0.0)
    expected_revenue = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    is_lost = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-id"]
        db_table = "deal"
        app_label = "deal"
