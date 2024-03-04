from django.db import models

from .base_model import BaseModel
from .processor import Processor


class BoxType(BaseModel):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50, blank=True, null=True)
    dimension = models.TextField(blank=True, null=True)
    processor = models.ForeignKey(Processor, on_delete=models.CASCADE)
    capacity = models.IntegerField(default=1)

    class Meta:
        db_table = 'box_type'
