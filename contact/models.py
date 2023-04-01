from django.db import models

from helpers.models import TrackingModel

# Create your models here.


class Contact(TrackingModel):
    owner = models.ForeignKey(to='authentication.User',
                              on_delete=models.CASCADE)
    country_code = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=30)
    contact_picture = models.URLField(null=True)
    is_favourite = models.BooleanField(default=True)
