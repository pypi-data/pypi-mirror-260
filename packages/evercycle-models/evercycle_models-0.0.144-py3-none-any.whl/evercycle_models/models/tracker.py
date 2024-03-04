from django.db import models
from .base_model import BaseModel
from .tracking import Tracking


class ShipmentStatus (models.TextChoices):
    unknown = ('unknown', 'Unknown'),
    in_transit = ('in_transit', 'In Transit'),
    out_for_delivery = ('out_for_delivery', 'Out for Delivery'),
    available_for_pickup = ('available_for_pickup', 'Available for pickup'),
    delivered = ('delivered', 'Delivered'),
    return_to_sender = ('return_to_sender', 'Return to Sender'),
    failure = ('failure', 'Failure'),
    canceled = ('canceled', 'Canceled'),
    error = ('error', 'Error')


class Tracker(BaseModel):
    tracking = models.ForeignKey(Tracking, on_delete=models.CASCADE)
    status = models.CharField(choices=ShipmentStatus.choices, default=ShipmentStatus.unknown)
    status_details = models.CharField(max_length=100, blank=True, null=True)
    status_date = models.DateTimeField()
    location_city = models.CharField(max_length=100, blank=True, null=True)
    location_state = models.CharField(max_length=100, blank=True, null=True)
    location_postal_code = models.CharField(max_length=100, blank=True, null=True)
    location_country = models.CharField(max_length=100, blank=True, null=True)
    meta_data = models.TextField(blank=True, null=True)
