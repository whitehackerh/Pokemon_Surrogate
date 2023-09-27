from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from api.Validators.SendMessageAcceptValidator import SendMessageAcceptValidator
from api.Services.SendMessageAcceptService import SendMessageAcceptService
from api.Responders.SendMessageAcceptResponder import SendMessageAcceptResponder
from api.Exceptions.CustomExceptions import CustomExceptions

class SendMessageAcceptView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            validator = SendMessageAcceptValidator(data=request.data)
            validator.is_valid(raise_exception=True)
            service = SendMessageAcceptService()
            data = service.service(request)
            responder = SendMessageAcceptResponder()
            responder.setResponse(data)
            return responder.getResponse()
        except CustomExceptions as e:
            responder = SendMessageAcceptResponder({'message': e.message, 'code': e.code})
            responder.setResponse()
            return responder.getResponse()