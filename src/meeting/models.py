from django.db import models

from account.models import Account
from authentication.models import User
from campaign.models import Campaign
from common.models import BaseModel, TimestampedModel
from contact.models import Contact
from deal.models import Deal
from lead.models import Lead

# Create your models here.


class Meeting(BaseModel):
    host = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="hosted_meetings"
    )

    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True, null=True)
    from_datetime = models.DateTimeField()
    to_datetime = models.DateTimeField()
    is_all_day = models.BooleanField(default=False)
    is_online_meeting = models.BooleanField(default=False)

    related_lead = models.ForeignKey(
        Lead, on_delete=models.SET_NULL, null=True, blank=True
    )
    related_contact = models.ForeignKey(
        Contact, on_delete=models.SET_NULL, null=True, blank=True
    )
    related_account = models.ForeignKey(
        Account, on_delete=models.SET_NULL, null=True, blank=True
    )
    related_campaign = models.ForeignKey(
        Campaign, on_delete=models.SET_NULL, null=True, blank=True
    )
    related_deal = models.ForeignKey(
        Deal, on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        ordering = ["-id"]
        db_table = "meeting"


class MeetingParticipant(TimestampedModel):
    meeting = models.ForeignKey(
        Meeting, on_delete=models.CASCADE, related_name="participants"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="meetings_participated",
    )
    contact = models.ForeignKey(
        Contact,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="meetings_participated",
    )
    lead = models.ForeignKey(
        Lead,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="meetings_participated",
    )

    class Meta:
        ordering = ["-id"]
        db_table = "meeting_participant"
