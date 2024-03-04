from django.db import models
from evercycle_models.models.base_model import BaseModel


class ServiceOrderType(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'service_order_type'
