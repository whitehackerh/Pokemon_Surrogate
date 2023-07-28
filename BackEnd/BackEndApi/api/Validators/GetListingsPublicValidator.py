from rest_framework import serializers
from django.core.validators import MinValueValidator

class GetListingsPublicValidator(serializers.Serializer):
    page = serializers.IntegerField(validators=[MinValueValidator(1)])