from django.db import models

from api.common import BaseModel
from deal.models import Stage, Deal


# Create your models here.


class StageHistory(BaseModel):
    stage = models.ForeignKey(Stage, on_delete=models.SET_NULL, null=True, blank=True, related_name="stage_history")
    deal = models.ForeignKey(Deal, on_delete=models.SET_NULL, null=True, blank=True, related_name="stage_history")

    class Meta:
        ordering = ["-id"]
        db_table = "stage_history"
        app_label = "stage_history"
