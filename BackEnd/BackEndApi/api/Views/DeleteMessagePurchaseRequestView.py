from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from api.Validators.DeleteMessagePurchaseRequestValidator import DeleteMessagePurchaseRequestValidator
from api.Services.DeleteMessagePurchaseRequestService import DeleteMessagePurchaseRequestService
from api.Responders.DeleteMessagePurchaseRequestResponder import DeleteMessagePurchaseRequestResponder
from api.Exceptions.CustomExceptions import CustomExceptions

class DeleteMessagePurchaseRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            validator = DeleteMessagePurchaseRequestValidator(data=request.data)
            validator.is_valid(raise_exception=True)
            service = DeleteMessagePurchaseRequestService()
            data = service.service(request.data)
            responder = DeleteMessagePurchaseRequestResponder()
            responder.setResponse(data)
            return responder.getResponse()
        except CustomExceptions as e:
            responder = DeleteMessagePurchaseRequestResponder({'message': e.message, 'code': e.code})
            responder.setResponse()
            return responder.getResponse()