from django.db import models


class Listing(models.Model):
    listing_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    profile_url = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=10)
    outcode = models.CharField(max_length=10)
    daily_price = models.DecimalField(max_digits=20, decimal_places=2)
    weekly_price = models.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        db_table = "listing"
