from django.db import models

from api import settings
from authentication.models import User
from common.models import BaseModel, BaseNameModel, CustomModel, TimestampedModel

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


class Lead(BaseModel, CustomModel):
    lead_owner = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="leads"
    )
    lead_source = models.ForeignKey(LeadSource, on_delete=models.SET_NULL, null=True)
    lead_status = models.ForeignKey(LeadStatus, on_delete=models.SET_NULL, null=True)
    industry = models.ForeignKey(Industry, on_delete=models.SET_NULL, null=True)

    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True, db_index=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    fax = models.CharField(max_length=20, null=True, blank=True)

    avatar = models.URLField(blank=True, null=True, default=settings.DEFAULT_AVATAR)
    annual_revenue = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True
    )

    is_email_opt_out = models.BooleanField(default=False)
    is_call_opt_out = models.BooleanField(default=False)

    street = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state_province = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)

    description = models.TextField(null=True, blank=True)

    #
    # SEARCH_FIELDS = {
    #
    #     "annual_revenue": ,
    # }

    SEARCH_FIELDS = dict(
        annual_revenue="annual_revenue",
    )

    SEARCH_FIELDS_CONTAINS = dict(
        first_name="first_name",
        last_name="last_name",
        company_name=company_name,
        email="email",
        phone="phone",
    )
    SORT_BY = ["first_name", "last_name", "company_name", "email"]

    class Meta:
        ordering = ["-id"]
        db_table = "lead"
        app_label = "lead"

    def get_full_name(self):
        try:
            full_name = f"{self.last_name} {self.first_name}"
        except AttributeError:
            full_name = self.email
        return full_name.strip()

    def get_data_contact_from_lead(self):
        return dict(
            lead_source=self.lead_source,
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            phone=self.phone,
            website=self.website,
            fax=self.fax,
            avatar=self.avatar,
            is_email_opt_out=self.is_email_opt_out,
            is_call_opt_out=self.is_call_opt_out,
            street=self.street,
            country=self.country,
            city=self.city,
            state_province=self.state_province,
            postal_code=self.postal_code,
            description=self.description,
        )

    def get_data_account_from_lead(self):
        return dict(
            convert_from=self,
            name=self.company_name,
            industry=self.industry,
            annual_revenue=self.annual_revenue,
            street=self.street,
            country=self.country,
            city=self.city,
            state_province=self.state_province,
            postal_code=self.postal_code,
            description=self.description,
        )
