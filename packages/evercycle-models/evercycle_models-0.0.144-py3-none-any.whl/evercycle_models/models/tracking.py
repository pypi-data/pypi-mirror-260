from django.db import models

from .base_model import BaseModel


class Tracking(BaseModel):
    tracking_number = models.CharField(max_length=50)
    label = models.CharField(max_length=100)
    last_retrack_date = models.DateTimeField()
    last_print_date = models.DateTimeField()
    archived = models.BooleanField(null=True, blank=True)
    step_number = models.IntegerField()
