from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from api.Validators.RemoveRequestValidator import RemoveRequestValidator
from api.Services.RemoveRequestService import RemoveRequestService
from api.Responders.RemoveRequestResponder import RemoveRequestResponder
from api.Exceptions.CustomExceptions import CustomExceptions

class RemoveRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            validator = RemoveRequestValidator(data=request.data)
            validator.is_valid(raise_exception=True)
            service = RemoveRequestService()
            data = service.service(request)
            responder = RemoveRequestResponder()
            responder.setResponse(data)
            return responder.getResponse()
        except CustomExceptions as e:
            responder = RemoveRequestResponder({'message': e.message, 'code': e.code})
            responder.setResponse()
            return responder.getResponse()