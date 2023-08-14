from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from api.Validators.RequestChangePricePurchaseRequestValidator import RequestChangePricePurchaseRequestValidator
from api.Services.RequestChangePricePurchaseRequestService import RequestChangePricePurchaseRequestService
from api.Responders.RequestChangePricePurchaseRequestResponder import RequestChangePricePurchaseRequestResponder
from api.Exceptions.CustomExceptions import CustomExceptions

class RequestChangePricePurchaseRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            validator = RequestChangePricePurchaseRequestValidator(data=request.data)
            validator.is_valid(raise_exception=True)
            service = RequestChangePricePurchaseRequestService()
            data = service.service(request.data)
            responder = RequestChangePricePurchaseRequestResponder()
            responder.setResponse(data)
            return responder.getResponse()
        except CustomExceptions as e:
            responder = RequestChangePricePurchaseRequestResponder({'message': e.message, 'code': e.code})
            responder.setResponse()
            return responder.getResponse()