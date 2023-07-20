from django.db import models
from api.Enums.ResponseCodes import ResponseCodes
from api.Exceptions.CustomExceptions import CustomExceptions

class ListingPictures(models.Model):
    listing_id = models.IntegerField()
    seller_id = models.IntegerField()
    path = models.CharField(max_length=255)
    sort_no = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        app_label = 'api'
        db_table = 'listing_pictures'

    def getListingPictures(self, listing_id):
        try:
            return ListingPictures.objects.filter(listing_id=listing_id, deleted_at__isnull=True).order_by('sort_no')
        except Exception as e:
            raise CustomExceptions(e, ResponseCodes.INTERNAL_SERVER_ERROR)