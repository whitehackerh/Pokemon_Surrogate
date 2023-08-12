from rest_framework import serializers

class GetPurchaseRequestDetailValidator(serializers.Serializer):
    purchase_request_id = serializers.IntegerField()
    user_id = serializers.IntegerField()