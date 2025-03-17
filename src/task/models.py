from django.db import models

from account.models import Account
from api.common import BaseModel, BaseNameModel
from authentication.models import User
from campaign.models import Campaign
from contact.models import Contact
from deal.models import Deal
from lead.models import Lead

# Create your models here.


class Priority(BaseNameModel):
    class Meta:
        ordering = ["-id"]
        db_table = "priority"


class TaskStatus(BaseNameModel):
    class Meta:
        ordering = ["-id"]
        db_table = "task_status"


class Task(BaseModel):
    task_owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="task_owner"
    )
    lead = models.ForeignKey(Lead, on_delete=models.SET_NULL, null=True, blank=True)
    contact = models.ForeignKey(
        Contact, on_delete=models.SET_NULL, null=True, blank=True, related_name="task"
    )
    related_account = models.ForeignKey(
        Account, on_delete=models.SET_NULL, null=True, blank=True, related_name="task"
    )
    related_deal = models.ForeignKey(
        Deal, on_delete=models.SET_NULL, null=True, blank=True, related_name="task"
    )
    related_campaign = models.ForeignKey(
        Campaign, on_delete=models.SET_NULL, null=True, blank=True, related_name="task"
    )
    priority = models.ForeignKey(
        Priority, on_delete=models.SET_NULL, null=True, blank=True
    )
    status = models.ForeignKey(
        TaskStatus, on_delete=models.SET_NULL, null=True, blank=True
    )

    title = models.CharField(max_length=255)
    due_date = models.DateField(null=True, blank=True)
    is_remind = models.BooleanField(default=False)
    is_repeat = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["-id"]
        db_table = "task"
        app_label = "task"
