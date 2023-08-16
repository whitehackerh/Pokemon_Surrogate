from rest_framework import serializers

class DeliverProductPurchaseRequestValidator(serializers.Serializer):
    purchase_request_id = serializers.IntegerField()
    seller_id = serializers.IntegerField()