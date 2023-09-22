from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from api.Validators.GetAcceptsValidator import GetAcceptsValidator
from api.Services.GetAcceptsService import GetAcceptsService
from api.Responders.GetAcceptsResponder import GetAcceptsResponder
from api.Exceptions.CustomExceptions import CustomExceptions

class GetAcceptsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            validator = GetAcceptsValidator(data=request.data)
            validator.is_valid(raise_exception=True)
            service = GetAcceptsService()
            data = service.service(request)
            responder = GetAcceptsResponder()
            responder.setResponse(data)
            return responder.getResponse()
        except CustomExceptions as e:
            responder = GetAcceptsResponder({'message': e.message, 'code': e.code})
            responder.setResponse()
            return responder.getResponse()