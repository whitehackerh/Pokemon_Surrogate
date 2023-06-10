from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from api.Enums.ResponseCodes import ResponseCodes
from api.Exceptions.CustomExceptions import CustomExceptions
from api.Services.BaseService import BaseService
from api.Enums.Path import Path

class SignupService(BaseService):
    def service(self, request):
        try:
            param = {
                'password': request.get('password'),
                'is_superuser': False,
                'username': request.get('username'),
                'first_name': request.get('first_name'),
                'last_name': request.get('last_name'),
                'email': request.get('email'),
                'is_staff': False,
                'is_active': True,
                'nickname': request.get('nickname'),
                'bank_account': request.get('bank_account'),
                'profile_picture': Path.DEFAULT_PROFILE_PICTURE,
            }
            usersModel = get_user_model()
            model = usersModel(**param)
            model.set_password(param['password'])
            model.save()

            data = {
                'token': Token.objects.create(user=model).key,
                'id': model.id,
                'username': model.username,
                'is_staff': model.is_staff
            }
            return data
        except Exception as e:
            raise CustomExceptions(e, ResponseCodes.INTERNAL_SERVER_ERROR)
