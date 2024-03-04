from django.db import models

from evercycle_models.models.base_model import BaseModel


class Contact(BaseModel):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.CharField(blank=True, null=True, max_length=100)

    class Meta:
        db_table = 'contact'
