from rest_framework import serializers
from api.models import Users

class LoginValidator(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()