from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from api.Validators.GetProfilePictureValidator import GetProfilePictureValidator
from api.Services.GetProfilePictureService import GetProfilePictureService
from api.Responders.GetProfilePictureResponder import GetProfilePictureResponder
from api.Exceptions.CustomExceptions import CustomExceptions

class GetProfilePictureView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            validator = GetProfilePictureValidator(data=request.data)
            validator.is_valid(raise_exception=True)
            service = GetProfilePictureService()
            data = service.service(request.data)
            responder = GetProfilePictureResponder()
            responder.setResponse(data)
            return responder.getResponse()
        except CustomExceptions as e:
            responder = GetProfilePictureResponder({'message': e.message, 'code': e.code})
            responder.setResponse()
            return responder.getResponse()