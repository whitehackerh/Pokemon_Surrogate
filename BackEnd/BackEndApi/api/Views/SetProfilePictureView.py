from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from api.Validators.SetProfilePictureValidator import SetProfilePictureValidator
from api.Services.SetProfilePictureService import SetProfilePictureService
from api.Responders.SetProfilePictureResponder import SetProfilePictureResponder
from api.Exceptions.CustomExceptions import CustomExceptions

class SetProfilePictureView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            validator = SetProfilePictureValidator(data=request.data)
            validator.is_valid(raise_exception=True)
            service = SetProfilePictureService()
            data = service.service(request)
            responder = SetProfilePictureResponder()
            responder.setResponse(data)
            return responder.getResponse()
        except CustomExceptions as e:
            responder = SetProfilePictureResponder({'message': e.message, 'code': e.code})
            responder.setResponse()
            return responder.getResponse()