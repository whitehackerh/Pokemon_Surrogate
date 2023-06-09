from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from api.Validators.GetUserProfileValidator import GetUserProfileValidator
from api.Services.GetUserProfileService import GetUserProfileService
from api.Responders.GetUserProfileResponder import GetUserProfileResponder
from api.Exceptions.CustomExceptions import CustomExceptions

class GetUserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            validator = GetUserProfileValidator(data=request.data)
            validator.is_valid(raise_exception=True)
            service = GetUserProfileService()
            data = service.service(request.data)
            responder = GetUserProfileResponder()
            responder.setResponse(data)
            return responder.getResponse()
        except CustomExceptions as e:
            responder = GetUserProfileResponder({'message': e.message, 'code': e.code})
            responder.setResponse()
            return responder.getResponse()