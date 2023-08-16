from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from api.Validators.DeliverProductPurchaseRequestValidator import DeliverProductPurchaseRequestValidator
from api.Services.DeliverProductPurchaseRequestService import DeliverProductPurchaseRequestService
from api.Responders.DeliverProductPurchaseRequestResponder import DeliverProductPurchaseRequestResponder
from api.Exceptions.CustomExceptions import CustomExceptions

class DeliverProductPurchaseRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            validator = DeliverProductPurchaseRequestValidator(data=request.data)
            validator.is_valid(raise_exception=True)
            service = DeliverProductPurchaseRequestService()
            data = service.service(request.data)
            responder = DeliverProductPurchaseRequestResponder()
            responder.setResponse(data)
            return responder.getResponse()
        except CustomExceptions as e:
            responder = DeliverProductPurchaseRequestResponder({'message': e.message, 'code': e.code})
            responder.setResponse()
            return responder.getResponse()