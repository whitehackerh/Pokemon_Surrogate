from rest_framework import serializers

class CancelTransactionPurchaseRequestValidator(serializers.Serializer):
    purchase_request_id = serializers.IntegerField()
    user_id = serializers.IntegerField()