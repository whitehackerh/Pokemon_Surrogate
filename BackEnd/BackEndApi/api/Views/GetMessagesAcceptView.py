from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from api.Validators.GetMessagesAcceptValidator import GetMessagesAcceptValidator
from api.Services.GetMessagesAcceptService import GetMessagesAcceptService
from api.Responders.GetMessagesAcceptResponder import GetMessagesAcceptResponder
from api.Exceptions.CustomExceptions import CustomExceptions

class GetMessagesAcceptView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            validator = GetMessagesAcceptValidator(data=request.data)
            validator.is_valid(raise_exception=True)
            service = GetMessagesAcceptService()
            data = service.service(request)
            responder = GetMessagesAcceptResponder()
            responder.setResponse(data)
            return responder.getResponse()
        except CustomExceptions as e:
            responder = GetMessagesAcceptResponder({'message': e.message, 'code': e.code})
            responder.setResponse()
            return responder.getResponse()