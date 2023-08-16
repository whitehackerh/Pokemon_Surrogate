from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from api.Validators.PayForPurchaseRequestValidator import PayForPurchaseRequestValidator
from api.Services.PayForPurchaseRequestService import PayForPurchaseRequestService
from api.Responders.PayForPurchaseRequestResponder import PayForPurchaseRequestResponder
from api.Exceptions.CustomExceptions import CustomExceptions

class PayForPurchaseRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            validator = PayForPurchaseRequestValidator(data=request.data)
            validator.is_valid(raise_exception=True)
            service = PayForPurchaseRequestService()
            data = service.service(request.data)
            responder = PayForPurchaseRequestResponder()
            responder.setResponse(data)
            return responder.getResponse()
        except CustomExceptions as e:
            responder = PayForPurchaseRequestResponder({'message': e.message, 'code': e.code})
            responder.setResponse()
            return responder.getResponse()