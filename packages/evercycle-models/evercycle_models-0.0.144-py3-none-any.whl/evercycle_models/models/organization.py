from django.db import models
from evercycle_models.models.address import Address
from evercycle_models.models.base_model import BaseModel
from evercycle_models.models.contact import Contact


class Organization(BaseModel):
    name = models.CharField(max_length=50)
    address = models.ForeignKey(Address, models.DO_NOTHING)
    parent_org = models.ForeignKey('self', on_delete=models.CASCADE, related_name='sub_organizations', null=True,
                                   blank=True)
    main_contact = models.ForeignKey(Contact, models.DO_NOTHING)
    tax_id = models.CharField(max_length=50)
    logo_image = models.BinaryField(blank=True, null=True)
    organization_type = models.TextField(blank=True, null=True)  # This field type is a guess.
    logo = models.CharField(max_length=256)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'organization'
