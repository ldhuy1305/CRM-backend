from django.db import models

from api.common import BaseModel, TimestampedModel
from authentication.models import User
from contact.models import Contact
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
        Contact, on_delete=models.SET_NULL, null=True, blank=True
    )
    lead = models.ForeignKey(Lead, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["-id"]
        db_table = "meeting_participant"
