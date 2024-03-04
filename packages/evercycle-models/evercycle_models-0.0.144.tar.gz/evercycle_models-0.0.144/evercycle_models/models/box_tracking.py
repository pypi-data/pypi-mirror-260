from django.db import models

from .base_model import BaseModel
from .box_type import BoxType
from .service_order import ServiceOrder
from .tracking import Tracking
from .box_status import BoxStatus


class BoxTracking(BaseModel):
    box_type = models.ForeignKey(BoxType, on_delete=models.CASCADE)
    service_order = models.ForeignKey(ServiceOrder, on_delete=models.CASCADE)
    outgoing_tracking = models.ForeignKey(
        Tracking, null=True, blank=True,
        on_delete=models.CASCADE,
        related_name='outgoing_tracking'
    )
    return_tracking_id = models.ForeignKey(
        Tracking, null=True, blank=True,
        on_delete=models.CASCADE,
        related_name='return_tracking'
    )
    box_status = models.ForeignKey(BoxStatus, null=True, blank=True, on_delete=models.CASCADE)

    archived = models.BooleanField(null=True, blank=True)
    service_order_uuid = models.CharField(max_length=20)
    error = models.TextField()

    class Meta:
        db_table = 'box_tracking'
