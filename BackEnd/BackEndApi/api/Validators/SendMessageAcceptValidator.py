from rest_framework import serializers
from django.core.validators import MinValueValidator

class SendMessageAcceptValidator(serializers.Serializer):
    accept_id = serializers.IntegerField()
    message = serializers.CharField(allow_null=True, allow_blank=True)