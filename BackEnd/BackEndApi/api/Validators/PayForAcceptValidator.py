from rest_framework import serializers

class PayForAcceptValidator(serializers.Serializer):
    accept_id = serializers.IntegerField()