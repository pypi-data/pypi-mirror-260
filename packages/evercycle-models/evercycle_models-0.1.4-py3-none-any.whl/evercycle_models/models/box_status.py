from django.db import models
from .base_model import BaseModel


class BoxStatus(BaseModel):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'box_status'
