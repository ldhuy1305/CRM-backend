from django.db import models

from common.models import BaseModel
from deal.models import Deal, Stage

# Create your models here.


class StageHistory(BaseModel):
    stage = models.ForeignKey(
        Stage,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="stage_history",
    )
    deal = models.ForeignKey(
        Deal,
        on_delete=models.CASCADE,
        related_name="stage_history",
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    probability = models.FloatField(default=0.0)
    expected_revenue = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    stage_duration = models.IntegerField(default=0)

    class Meta:
        ordering = ["-id"]
        db_table = "stage_history"
        app_label = "stage_history"

    def save(self, *args, **kwargs):
        if self.deal and self.stage:
            last_stage = (
                StageHistory.objects.filter(deal=self.deal)
                .exclude(id=self.id)
                .order_by("-created_at")
                .first()
            )

            if last_stage:
                self.stage_duration = (
                    self.created_at.date() - last_stage.created_at.date()
                ).days

        super().save(*args, **kwargs)
