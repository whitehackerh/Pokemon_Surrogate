from django.db import models
from api.Enums.ResponseCodes import ResponseCodes
from api.Exceptions.CustomExceptions import CustomExceptions
from django.db.models import Subquery, OuterRef
from django.utils import timezone

class PurchaseRequestMessages(models.Model):
    purchase_request_id = models.IntegerField()
    sender_id = models.IntegerField()
    message = models.TextField(null=True)
    picture = models.CharField(null=True, max_length=255)
    read = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        app_label = 'api'
        db_table = 'purchase_request_messages'

    def getPictures(self, purchase_request_id):
        try:
            return PurchaseRequestMessages.objects.only('picture').filter(purchase_request_id=purchase_request_id)
        except Exception as e:
            raise CustomExceptions(e, ResponseCodes.INTERNAL_SERVER_ERROR)
    
    def setPicture(self, id, filename):
        try:
            message = PurchaseRequestMessages.objects.get(id=id)
            message.picture = filename
            message.save()
        except Exception as e:
            raise CustomExceptions(e, ResponseCodes.INTERNAL_SERVER_ERROR)