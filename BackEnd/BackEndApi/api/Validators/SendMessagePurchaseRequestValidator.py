from rest_framework import serializers
from django.core.validators import MinValueValidator

class SendMessagePurchaseRequestValidator(serializers.Serializer):
    purchase_request_id = serializers.IntegerField()
    sender_id = serializers.IntegerField()
    message = serializers.CharField(allow_null=True)