from rest_framework import serializers

class PayForPurchaseRequestValidator(serializers.Serializer):
    purchase_request_id = serializers.IntegerField()
    buyer_id = serializers.IntegerField()