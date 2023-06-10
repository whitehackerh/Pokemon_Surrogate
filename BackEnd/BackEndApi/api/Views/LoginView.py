from rest_framework.views import APIView
from rest_framework import serializers
from api.Validators.LoginValidator import LoginValidator
from api.Services.LoginService import LoginService
from api.Responders.LoginResponder import LoginResponder
from api.Enums.ResponseCodes import ResponseCodes
from api.Exceptions.CustomExceptions import CustomExceptions

class LoginView(APIView):
    permission_classes = []

    def post(self, request):
        try:
            validator = LoginValidator(data=request.data)
            validator.is_valid(raise_exception=True)
            service = LoginService()
            data = service.service(request.data)
            responder = LoginResponder()
            responder.setResponse(data)
            return responder.getResponse()
        except serializers.ValidationError as e:
            responder = LoginResponder({'message': e.detail, 'code': ResponseCodes.VALIDATION_ERROR})
            responder.setResponse()
            return responder.getResponse()
        except CustomExceptions as e:
            responder = LoginResponder({'message': e.message, 'code': e.code})
            responder.setResponse()
            return responder.getResponse()