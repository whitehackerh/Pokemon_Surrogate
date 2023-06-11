from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from api.Validators.SetUserInfoValidator import SetUserInfoValidator
from api.Services.SetUserInfoService import SetUserInfoService
from api.Responders.SetUserInfoResponder import SetUserInfoResponder
from api.Enums.ResponseCodes import ResponseCodes
from api.Exceptions.CustomExceptions import CustomExceptions

class SetUserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            validator = SetUserInfoValidator(data=request.data)
            validator.is_valid(raise_exception=True)
            service = SetUserInfoService()
            data = service.service(request.data)
            responder = SetUserInfoResponder()
            responder.setResponse(data)
            return responder.getResponse()
        except serializers.ValidationError as e:
            responder = SetUserInfoResponder({'message': e.detail, 'code': ResponseCodes.VALIDATION_ERROR})
            responder.setResponse()
            return responder.getResponse()
        except CustomExceptions as e:
            responder = SetUserInfoResponder({'message': e.message, 'code': e.code})
            responder.setResponse()
            return responder.getResponse()