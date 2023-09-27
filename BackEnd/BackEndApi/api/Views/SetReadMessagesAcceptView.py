from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from api.Validators.SetReadMessagesAcceptValidator import SetReadMessagesAcceptValidator
from api.Services.SetReadMessagesAcceptService import SetReadMessagesAcceptService
from api.Responders.SetReadMessagesAcceptResponder import SetReadMessagesAcceptResponder
from api.Exceptions.CustomExceptions import CustomExceptions

class SetReadMessagesAcceptView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            validator = SetReadMessagesAcceptValidator(data=request.data)
            validator.is_valid(raise_exception=True)
            service = SetReadMessagesAcceptService()
            data = service.service(request)
            responder = SetReadMessagesAcceptResponder()
            responder.setResponse(data)
            return responder.getResponse()
        except CustomExceptions as e:
            responder = SetReadMessagesAcceptResponder({'message': e.message, 'code': e.code})
            responder.setResponse()
            return responder.getResponse()