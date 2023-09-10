from rest_framework import serializers
from django.core.validators import MinValueValidator

class GetRequestsValidator(serializers.Serializer):
    page = serializers.IntegerField(validators=[MinValueValidator(1)])
    status = serializers.IntegerField(allow_null=True)