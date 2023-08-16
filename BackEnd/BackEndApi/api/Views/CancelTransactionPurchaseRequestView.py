from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from api.Validators.CancelTransactionPurchaseRequestValidator import CancelTransactionPurchaseRequestValidator
from api.Services.CancelTransactionPurchaseRequestService import CancelTransactionPurchaseRequestService
from api.Responders.CancelTransactionPurchaseRequestResponder import CancelTransactionPurchaseRequestResponder
from api.Exceptions.CustomExceptions import CustomExceptions

class CancelTransactionPurchaseRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            validator = CancelTransactionPurchaseRequestValidator(data=request.data)
            validator.is_valid(raise_exception=True)
            service = CancelTransactionPurchaseRequestService()
            data = service.service(request.data)
            responder = CancelTransactionPurchaseRequestResponder()
            responder.setResponse(data)
            return responder.getResponse()
        except CustomExceptions as e:
            responder = CancelTransactionPurchaseRequestResponder({'message': e.message, 'code': e.code})
            responder.setResponse()
            return responder.getResponse()