from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework import serializers
from api.Validators.SignupStaffValidator import SignupStaffValidator
from api.Services.SignupStaffService import SignupStaffService
from api.Responders.SignupStaffResponder import SignupStaffResponder
from api.Enums.ResponseCodes import ResponseCodes
from api.Exceptions.CustomExceptions import CustomExceptions

class SignupStaffView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        try:
            validator = SignupStaffValidator(data=request.data)
            validator.is_valid(raise_exception=True)
            validated_data = validator.validated_data
            validator.customValidation(validated_data)
            service = SignupStaffService()
            data = service.service(request.data)
            responder = SignupStaffResponder()
            responder.setResponse(data)
            return responder.getResponse()
        except serializers.ValidationError as e:
            responder = SignupStaffResponder({'message': e.detail, 'code': ResponseCodes.VALIDATION_ERROR})
            responder.setResponse()
            return responder.getResponse()
        except CustomExceptions as e:
            responder = SignupStaffResponder({'message': e.message, 'code': e.code})
            responder.setResponse()
            return responder.getResponse()