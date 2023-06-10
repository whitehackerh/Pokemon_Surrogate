from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from api.Enums.ResponseCodes import ResponseCodes
from api.Exceptions.CustomExceptions import CustomExceptions
from api.Services.BaseService import BaseService

class LoginService(BaseService):
    def service(self, request):
        try:
            data = {}

            user = authenticate(username=request.get('username'), password=request.get('password'))
            if user is not None:
                token, _ = Token.objects.get_or_create(user=user)
                data = {
                    'token': token.key,
                    'id': user.id,
                    'username': user.username,
                    'is_staff': user.is_staff
                }
            else:
                data = {
                    'error': 'Invalid username or password.'
                }
            return data
        except Exception as e:
            raise CustomExceptions(e, ResponseCodes.INTERNAL_SERVER_ERROR)