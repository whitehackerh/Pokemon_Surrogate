from rest_framework import serializers

class ResponseChangePricePurchaseRequestValidator(serializers.Serializer):
    purchase_request_id = serializers.IntegerField()
    seller_id = serializers.IntegerField()
    response = serializers.BooleanField()