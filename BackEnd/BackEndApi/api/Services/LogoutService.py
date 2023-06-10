from rest_framework.authtoken.models import Token
from api.Enums.ResponseCodes import ResponseCodes
from api.Exceptions.CustomExceptions import CustomExceptions
from api.Services.BaseService import BaseService

class LogoutService(BaseService):
    def service(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION').split()[1]
            Token.objects.filter(key=token).delete()
            return None
        except Exception as e:
            raise CustomExceptions(e, ResponseCodes.INTERNAL_SERVER_ERROR)