from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from api.Validators.SetRequestValidator import SetRequestValidator
from api.Services.SetRequestService import SetRequestService
from api.Responders.SetRequestResponder import SetRequestResponder
from api.Exceptions.CustomExceptions import CustomExceptions

class SetRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            validator = SetRequestValidator(data=request.data)
            validator.is_valid(raise_exception=True)
            service = SetRequestService()
            data = service.service(request)
            responder = SetRequestResponder()
            responder.setResponse(data)
            return responder.getResponse()
        except CustomExceptions as e:
            responder = SetRequestResponder({'message': e.message, 'code': e.code})
            responder.setResponse()
            return responder.getResponse()