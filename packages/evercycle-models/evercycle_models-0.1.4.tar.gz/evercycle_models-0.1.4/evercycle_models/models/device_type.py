from django.db import models

from evercycle_models.models.base_model import BaseModel


class DeviceType(BaseModel):
    type = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.id } - {self.type}"

    class Meta:
        db_table = 'device_type'
