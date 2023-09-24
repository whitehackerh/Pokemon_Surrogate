from rest_framework import serializers
from django.core.validators import MinValueValidator

class RequestPriceAcceptValidator(serializers.Serializer):
    accept_id = serializers.IntegerField()
    request_price = serializers.IntegerField(validators=[MinValueValidator(1)])