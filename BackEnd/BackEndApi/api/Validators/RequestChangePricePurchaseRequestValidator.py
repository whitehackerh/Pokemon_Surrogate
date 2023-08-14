from rest_framework import serializers
from django.core.validators import MinValueValidator

class RequestChangePricePurchaseRequestValidator(serializers.Serializer):
    purchase_request_id = serializers.IntegerField()
    buyer_id = serializers.IntegerField()
    request_price = serializers.IntegerField(validators=[MinValueValidator(1)])