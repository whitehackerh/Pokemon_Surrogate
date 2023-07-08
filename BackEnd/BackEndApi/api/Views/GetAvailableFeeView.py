from rest_framework.views import APIView
from api.Validators.GetAvailableFeeValidator import GetAvailableFeeValidator
from api.Services.GetAvailableFeeService import GetAvailableFeeService
from api.Responders.GetAvailableFeeResponder import GetAvailableFeeResponder
from api.Exceptions.CustomExceptions import CustomExceptions

class GetAvailableFeeView(APIView):
    permission_classes = []

    def get(self, request):
        try:
            GetAvailableFeeValidator()
            service = GetAvailableFeeService()
            data = service.service()
            responder = GetAvailableFeeResponder()
            responder.setResponse(data)
            return responder.getResponse()
        except CustomExceptions as e:
            responder = GetAvailableFeeResponder({'message': e.message, 'code': e.code})
            responder.setResponse()
            return responder.getResponse()