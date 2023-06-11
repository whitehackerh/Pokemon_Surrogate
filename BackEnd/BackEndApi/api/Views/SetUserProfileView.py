from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from api.Validators.SetUserProfileValidator import SetUserProfileValidator
from api.Services.SetUserProfileService import SetUserProfileService
from api.Responders.SetUserProfileResponder import SetUserProfileResponder
from api.Enums.ResponseCodes import ResponseCodes
from api.Exceptions.CustomExceptions import CustomExceptions

class SetUserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            validator = SetUserProfileValidator(data=request.data)
            validator.is_valid(raise_exception=True)
            service = SetUserProfileService()
            data = service.service(request.data)
            responder = SetUserProfileResponder()
            responder.setResponse(data)
            return responder.getResponse()
        except serializers.ValidationError as e:
            responder = SetUserProfileResponder({'message': e.detail, 'code': ResponseCodes.VALIDATION_ERROR})
            responder.setResponse()
            return responder.getResponse()
        except CustomExceptions as e:
            responder = SetUserProfileResponder({'message': e.message, 'code': e.code})
            responder.setResponse()
            return responder.getResponse()