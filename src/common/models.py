from django.db import models
from django.utils import timezone


class TimestampedModel(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True


class BaseModel(TimestampedModel):
    created_by = models.ForeignKey(
        "authentication.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="%(app_label)s_created_by",
    )
    updated_by = models.ForeignKey(
        "authentication.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="%(app_label)s_updated_by",
    )

    class Meta:
        abstract = True


class CustomManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class CustomModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        if not self.is_deleted:
            self.is_deleted = True
            self.deleted_at = timezone.now()
            self.save()

    objects = CustomManager()


class BaseNameModel(TimestampedModel):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name
