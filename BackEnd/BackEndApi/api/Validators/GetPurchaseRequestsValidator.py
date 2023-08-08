from rest_framework import serializers
from django.core.validators import MinValueValidator

class GetPurchaseRequestsValidator(serializers.Serializer):
    status = serializers.IntegerField()
    seller_id = serializers.IntegerField(allow_null=True)
    buyer_id = serializers.IntegerField(allow_null=True)
    page = serializers.IntegerField(validators=[MinValueValidator(1)])