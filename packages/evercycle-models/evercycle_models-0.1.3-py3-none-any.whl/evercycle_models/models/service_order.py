from django.db import models

from evercycle_models.models import Workflow, Address, Contact
from evercycle_models.models.base_model import BaseModel
from evercycle_models.models.service_order_type import ServiceOrderType


class ServiceOrder(BaseModel):
    reference = models.CharField(max_length=100, default='Unknown')
    ship_to_address = models.ForeignKey(Address, models.DO_NOTHING, default='Unknown')

    contact = models.ForeignKey(Contact, models.DO_NOTHING, default='Unknown')
    workflow = models.ForeignKey(Workflow, models.DO_NOTHING, default='Unknown')
    service_order_type = models.ForeignKey(ServiceOrderType, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'service_order'
