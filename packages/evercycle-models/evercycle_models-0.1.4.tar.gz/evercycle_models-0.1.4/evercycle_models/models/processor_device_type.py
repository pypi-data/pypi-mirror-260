from django.db import models

from .base_model import BaseModel
from .processor import Processor
from .device_type import DeviceType


class ProcessorDeviceType(BaseModel):
    type = models.ForeignKey(DeviceType, models.DO_NOTHING)
    description = models.CharField(max_length=50)
    processor = models.ForeignKey(Processor, on_delete=models.CASCADE)
    outbound_ship_weight = models.IntegerField()
    return_ship_weight = models.IntegerField()

    def __str__(self):
        return f"{self.id } - {self.type.type} {self.description}"

    class Meta:
        db_table = 'processor_device_type'
