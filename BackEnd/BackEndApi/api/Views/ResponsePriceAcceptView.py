from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from api.Validators.ResponsePriceAcceptValidator import ResponsePriceAcceptValidator
from api.Services.ResponsePriceAcceptService import ResponsePriceAcceptService
from api.Responders.ResponsePriceAcceptResponder import ResponsePriceAcceptResponder
from api.Exceptions.CustomExceptions import CustomExceptions

class ResponsePriceAcceptView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            validator = ResponsePriceAcceptValidator(data=request.data)
            validator.is_valid(raise_exception=True)
            service = ResponsePriceAcceptService()
            data = service.service(request)
            responder = ResponsePriceAcceptResponder()
            responder.setResponse(data)
            return responder.getResponse()
        except CustomExceptions as e:
            responder = ResponsePriceAcceptResponder({'message': e.message, 'code': e.code})
            responder.setResponse()
            return responder.getResponse()