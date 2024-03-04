from django.db import models


class Address(models.Model):

    unique_key = models.CharField(max_length=100, default='')
    street = models.CharField(max_length=50)
    secondary = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=50)

    def __str__(self):
        return (f"{self.street} {self.secondary} {self.city} "
                f"{self.state} {self.postal_code} {self.country}")

    class Meta:
        db_table = 'address'
