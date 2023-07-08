from django.db import models

class Listing(models.Model):
    seller_id = models.IntegerField()
    game_title_id = models.IntegerField()
    category = models.IntegerField()
    listing_title = models.CharField(max_length=255)
    description = models.TextField()
    price_negotiation = models.IntegerField()
    price = models.IntegerField()
    fee_id = models.IntegerField()
    status = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        app_label = 'api'
        db_table = 'listing'