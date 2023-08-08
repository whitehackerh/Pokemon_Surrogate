from rest_framework import serializers

class GetPurchaseRequestsSummaryValidator(serializers.Serializer):
    seller_id = serializers.IntegerField(allow_null=True)
    buyer_id = serializers.IntegerField(allow_null=True)
    status = serializers.IntegerField()