from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from api.Validators.CompleteTransactionPurchaseRequestValidator import CompleteTransactionPurchaseRequestValidator
from api.Services.CompleteTransactionPurchaseRequestService import CompleteTransactionPurchaseRequestService
from api.Responders.CompleteTransactionPurchaseRequestResponder import CompleteTransactionPurchaseRequestResponder
from api.Exceptions.CustomExceptions import CustomExceptions

class CompleteTransactionPurchaseRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            validator = CompleteTransactionPurchaseRequestValidator(data=request.data)
            validator.is_valid(raise_exception=True)
            service = CompleteTransactionPurchaseRequestService()
            data = service.service(request.data)
            responder = CompleteTransactionPurchaseRequestResponder()
            responder.setResponse(data)
            return responder.getResponse()
        except CustomExceptions as e:
            responder = CompleteTransactionPurchaseRequestResponder({'message': e.message, 'code': e.code})
            responder.setResponse()
            return responder.getResponse()