from django.db import models

from evercycle_models.models import Workflow, Address, Contact
from evercycle_models.models.base_model import BaseModel


class ServiceOrder(BaseModel):
    reference = models.CharField(max_length=100, default='Unknown')
    ship_to_address = models.ForeignKey(Address, models.DO_NOTHING, default='Unknown')
    request_type = models.CharField(max_length=10, default='Unknown')

    contact = models.ForeignKey(Contact, models.DO_NOTHING, default='Unknown')
    workflow = models.ForeignKey(Workflow, models.DO_NOTHING, default='Unknown')

    class Meta:
        db_table = 'service_order'
