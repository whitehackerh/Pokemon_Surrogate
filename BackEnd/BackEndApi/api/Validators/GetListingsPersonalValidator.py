from rest_framework import serializers
from django.core.validators import MinValueValidator

class GetListingsPersonalValidator(serializers.Serializer):
    seller_id = serializers.IntegerField()
    page = serializers.IntegerField(validators=[MinValueValidator(1)])
    status = serializers.IntegerField()