from rest_framework import serializers
from django.core.validators import MinValueValidator

class GetAcceptsValidator(serializers.Serializer):
    status = serializers.IntegerField()
    client = serializers.BooleanField()
    page = serializers.IntegerField(validators=[MinValueValidator(1)])