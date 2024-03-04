from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.CharField(max_length=150, default="1")
    updated_by = models.CharField(max_length=150, null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True
