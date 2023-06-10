from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from api.Validators.LogoutValidator import LogoutValidator
from api.Services.LogoutService import LogoutService
from api.Responders.LogoutResponder import LogoutResponder
from api.Exceptions.CustomExceptions import CustomExceptions

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            LogoutValidator()
            service = LogoutService()
            data = service.service(request)
            responder = LogoutResponder()
            responder.setResponse(data)
            return responder.getResponse()
        except CustomExceptions as e:
            responder = LogoutResponder({'message': e.message, 'code': e.code})
            responder.setResponse()
            return responder.getResponse()