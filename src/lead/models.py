from django.db import models

from api import settings
from api.common import BaseModel, BaseNameModel, TimestampedModel
from authentication.models import User

# Create your models here.


class LeadSource(BaseNameModel):
    class Meta:
        ordering = ["-id"]
        db_table = "lead_source"


class LeadStatus(BaseNameModel):
    class Meta:
        ordering = ["-id"]
        db_table = "lead_status"


class Industry(BaseNameModel):
    class Meta:
        ordering = ["-id"]
        db_table = "industry"


class Lead(BaseModel):
    lead_owner = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="leads"
    )
    lead_source = models.ForeignKey(LeadSource, on_delete=models.SET_NULL, null=True)
    lead_status = models.ForeignKey(LeadStatus, on_delete=models.SET_NULL, null=True)
    industry = models.ForeignKey(Industry, on_delete=models.SET_NULL, null=True)

    name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    fax = models.CharField(max_length=20, null=True, blank=True)

    avatar = models.URLField(blank=True, null=True, default=settings.DEFAULT_AVATAR)
    annual_revenue = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True
    )

    is_email_opt_out = models.BooleanField(default=False)
    is_call_opt_out = models.BooleanField(default=False)

    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state_province = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)

    description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ["-id"]
        db_table = "lead"
        app_label = "lead"
