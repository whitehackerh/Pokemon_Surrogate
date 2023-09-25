from rest_framework import serializers

class CompleteTransactionAcceptValidator(serializers.Serializer):
    accept_id = serializers.IntegerField()