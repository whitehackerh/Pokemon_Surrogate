from rest_framework import serializers

class CancelTransactionAcceptValidator(serializers.Serializer):
    accept_id = serializers.IntegerField()