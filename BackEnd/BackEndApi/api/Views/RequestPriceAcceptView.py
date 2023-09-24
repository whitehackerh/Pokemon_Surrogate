from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from api.Validators.RequestPriceAcceptValidator import RequestPriceAcceptValidator
from api.Services.RequestPriceAcceptService import RequestPriceAcceptService
from api.Responders.RequestPriceAcceptResponder import RequestPriceAcceptResponder
from api.Exceptions.CustomExceptions import CustomExceptions

class RequestPriceAcceptView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            validator = RequestPriceAcceptValidator(data=request.data)
            validator.is_valid(raise_exception=True)
            service = RequestPriceAcceptService()
            data = service.service(request)
            responder = RequestPriceAcceptResponder()
            responder.setResponse(data)
            return responder.getResponse()
        except CustomExceptions as e:
            responder = RequestPriceAcceptResponder({'message': e.message, 'code': e.code})
            responder.setResponse()
            return responder.getResponse()