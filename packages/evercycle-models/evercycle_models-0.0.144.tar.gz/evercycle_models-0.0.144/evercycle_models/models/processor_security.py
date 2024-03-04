from django.db import models

from evercycle_models.models.base_model import BaseModel


class ProcessorSecurity(BaseModel):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'processor_security'
