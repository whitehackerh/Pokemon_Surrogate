from rest_framework.views import APIView
from rest_framework import serializers
from api.Validators.SignupValidator import SignupValidator
from api.Services.SignupService import SignupService
from api.Responders.SignupResponder import SignupResponder
from api.Enums.ResponseCodes import ResponseCodes
from api.Exceptions.CustomExceptions import CustomExceptions

class SignupView(APIView):
    permission_classes = []

    def post(self, request):
        try:
            validator = SignupValidator(data=request.data)
            validator.is_valid(raise_exception=True)
            validated_data = validator.validated_data
            validator.customValidation(validated_data)
            service = SignupService()
            data = service.service(request.data)
            responder = SignupResponder()
            responder.setResponse(data)
            return responder.getResponse()
        except serializers.ValidationError as e:
            responder = SignupResponder({'message': e.detail, 'code': ResponseCodes.VALIDATION_ERROR})
            responder.setResponse()
            return responder.getResponse()
        except CustomExceptions as e:
            responder = SignupResponder({'message': e.message, 'code': e.code})
            responder.setResponse()
            return responder.getResponse()

            