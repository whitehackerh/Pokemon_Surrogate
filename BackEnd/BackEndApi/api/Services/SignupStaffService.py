from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from api.Enums.ResponseCodes import ResponseCodes
from api.Exceptions.CustomExceptions import CustomExceptions
from api.Services.BaseService import BaseService
from api.Enums.Path import Path

class SignupStaffService(BaseService):
    def service(self, request):
        try:
            param = {
                'password': request.get('password'),
                'is_superuser': False,
                'username': request.get('username'),
                'first_name': request.get('first_name'),
                'last_name': request.get('last_name'),
                'email': request.get('email'),
                'is_staff': True,
                'is_active': True,
                'nickname': request.get('nickname'),
                'bank_account': request.get('bank_account'),
                'profile_picture': Path.DEFAULT_PROFILE_PICTURE,
            }
            usersModel = get_user_model()
            model = usersModel(**param)
            model.set_password(param['password'])
            model.save()

            Token.objects.create(user=model).key

            return None
        except Exception as e:
            raise CustomExceptions(e, ResponseCodes.INTERNAL_SERVER_ERROR)
