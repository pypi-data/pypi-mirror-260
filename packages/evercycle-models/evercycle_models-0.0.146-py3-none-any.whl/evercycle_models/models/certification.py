from django.db import models

from evercycle_models.models.base_model import BaseModel


class Certification(BaseModel):
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=50)

    class Meta:
        db_table = 'certification'
