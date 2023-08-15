from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from api.Validators.ResponseChangePricePurchaseRequestValidator import ResponseChangePricePurchaseRequestValidator
from api.Services.ResponseChangePricePurchaseRequestService import ResponseChangePricePurchaseRequestService
from api.Responders.ResponseChangePricePurchaseRequestResponder import ResponseChangePricePurchaseRequestResponder
from api.Exceptions.CustomExceptions import CustomExceptions

class ResponseChangePricePurchaseRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            validator = ResponseChangePricePurchaseRequestValidator(data=request.data)
            validator.is_valid(raise_exception=True)
            service = ResponseChangePricePurchaseRequestService()
            data = service.service(request.data)
            responder = ResponseChangePricePurchaseRequestResponder()
            responder.setResponse(data)
            return responder.getResponse()
        except CustomExceptions as e:
            responder = ResponseChangePricePurchaseRequestResponder({'message': e.message, 'code': e.code})
            responder.setResponse()
            return responder.getResponse()