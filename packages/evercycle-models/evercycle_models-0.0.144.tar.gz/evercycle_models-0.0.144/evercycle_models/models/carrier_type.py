from django.db import models

from evercycle_models.models.base_model import BaseModel


class CarrierType(BaseModel):
    name = models.CharField(max_length=50)
    f_id = models.CharField(max_length=100)
    account_type_id = models.CharField(max_length=50)
    account_type = models.CharField(max_length=50)

    class Meta:
        db_table = 'carrier_type'
