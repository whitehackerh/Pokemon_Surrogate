from rest_framework import serializers

class DeleteMessagePurchaseRequestValidator(serializers.Serializer):
    message_id = serializers.IntegerField()
    purchase_request_id = serializers.IntegerField()
    sender_id = serializers.IntegerField()