from rest_framework import serializers
from api.models import Users
from api.Enums.Messages import Messages
from api.Enums.ResponseCodes import ResponseCodes
from api.Exceptions.CustomExceptions import CustomExceptions

class SignupValidator(serializers.Serializer):
    password = serializers.CharField(max_length=128)
    username = serializers.CharField(max_length=150)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    nickname = serializers.CharField(max_length=255)
    bank_account = serializers.CharField(max_length=100)

    def customValidation(self, request):
        self.validateUsername(request.get('username'))
        self.validateEmail(request.get('email'))
    
    def validateUsername(self, value):
        if Users.objects.filter(username=value).exists():
            raise CustomExceptions(Messages.USERNAME_ALREADY_USE, ResponseCodes.VALIDATION_ERROR)

    def validateEmail(self, value):
        if Users.objects.filter(email=value).exists():
            raise CustomExceptions(Messages.EMAIL_ALREADY_USE, ResponseCodes.VALIDATION_ERROR)

