from django.db import models
from .address import Address
from .base_model import BaseModel
from .contact import Contact


class Processor(BaseModel):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    address = models.ForeignKey(Address, models.DO_NOTHING)
    contact = models.ForeignKey(Contact, models.DO_NOTHING)

    class Meta:
        db_table = 'processor'
