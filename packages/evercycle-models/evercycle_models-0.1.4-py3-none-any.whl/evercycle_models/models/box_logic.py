from django.db import models

from .base_model import BaseModel
from .organization import Organization
from .processor import Processor


class BoxLogic(BaseModel):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    processor = models.ForeignKey(Processor, on_delete=models.CASCADE)
    box_configuration = models.TextField()

    class Meta:
        db_table = 'box_logic'
