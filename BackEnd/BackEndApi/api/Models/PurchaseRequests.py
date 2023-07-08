from django.db import models

class PurchaseRequests(models.Model):
    listing_id = models.IntegerField()
    seller_id = models.IntegerField()
    buyer_id = models.IntegerField()
    price = models.IntegerField()
    status = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        app_label = 'api'
        db_table = 'purchase_requests'