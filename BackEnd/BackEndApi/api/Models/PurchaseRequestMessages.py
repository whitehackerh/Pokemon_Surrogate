from django.db import models
from api.Enums.ResponseCodes import ResponseCodes
from api.Enums.Read import Read
from api.Exceptions.CustomExceptions import CustomExceptions
from django.utils import timezone
from django.db.models import Q

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
    
    def getMessages(self, purchase_request_id):
        try:
            return PurchaseRequestMessages.objects.filter(purchase_request_id=purchase_request_id, deleted_at__isnull=True).order_by('id')
        except Exception as e:
            raise CustomExceptions(e, ResponseCodes.INTERNAL_SERVER_ERROR)
    
    def getMessagesLatest(self, purchase_request_id, id):
        try:
            return PurchaseRequestMessages.objects.filter(purchase_request_id=purchase_request_id, deleted_at__isnull=True, id__gt=id).order_by('id')
        except Exception as e:
            raise CustomExceptions(e, ResponseCodes.INTERNAL_SERVER_ERROR)
    
    def setReadMessages(self, purchase_request_id, user_id, id):
        try:
            PurchaseRequestMessages.objects.filter(
                ~Q(sender_id=user_id)
                & Q(id__lte=id),
                purchase_request_id=purchase_request_id,
            ).update(read=Read.READ)
        except Exception as e:
            raise CustomExceptions(str(e), ResponseCodes.INTERNAL_SERVER_ERROR)
        
    def getMessage(self, id):
        try:
            return PurchaseRequestMessages.objects.get(id=id)
        except Exception as e:
            raise CustomExceptions(e, ResponseCodes.INTERNAL_SERVER_ERROR)