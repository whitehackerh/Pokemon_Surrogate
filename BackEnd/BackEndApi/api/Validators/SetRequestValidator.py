from rest_framework import serializers
from django.core.validators import MinValueValidator

class SetRequestValidator(serializers.Serializer):
    request_id = serializers.IntegerField(allow_null=True)
    game_title_id = serializers.IntegerField()
    category = serializers.IntegerField()
    request_title = serializers.CharField(max_length=255)
    description = serializers.CharField()
    min_price = serializers.IntegerField(validators=[MinValueValidator(1)])
    max_price = serializers.IntegerField(validators=[MinValueValidator(1)])