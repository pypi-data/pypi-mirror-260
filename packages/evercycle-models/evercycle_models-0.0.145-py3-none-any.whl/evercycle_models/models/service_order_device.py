from django.db import models

from .base_model import BaseModel
from .service_order import ServiceOrder
from .processor_device_type import ProcessorDeviceType


class ServiceOrderDevice(BaseModel):

    service_order = models.ForeignKey(ServiceOrder, on_delete=models.DO_NOTHING)
    processor_device_type = models.ForeignKey(ProcessorDeviceType, on_delete=models.DO_NOTHING)
    disposition_status = models.CharField(max_length=50)
    serial_number = models.CharField(max_length=50)

    class Meta:
        db_table = 'service_order_device'
