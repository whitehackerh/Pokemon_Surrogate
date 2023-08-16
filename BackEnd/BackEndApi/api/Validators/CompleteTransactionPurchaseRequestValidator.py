from rest_framework import serializers

class CompleteTransactionPurchaseRequestValidator(serializers.Serializer):
    purchase_request_id = serializers.IntegerField()
    buyer_id = serializers.IntegerField()