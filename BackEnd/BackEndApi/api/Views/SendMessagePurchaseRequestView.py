from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from api.Validators.SendMessagePurchaseRequestValidator import SendMessagePurchaseRequestValidator
from api.Services.SendMessagePurchaseRequestService import SendMessagePurchaseRequestService
from api.Responders.SendMessagePurchaseRequestResponder import SendMessagePurchaseRequestResponder
from api.Exceptions.CustomExceptions import CustomExceptions

class SendMessagePurchaseRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            validator = SendMessagePurchaseRequestValidator(data=request.data)
            validator.is_valid(raise_exception=True)
            service = SendMessagePurchaseRequestService()
            data = service.service(request)
            responder = SendMessagePurchaseRequestResponder()
            responder.setResponse(data)
            return responder.getResponse()
        except CustomExceptions as e:
            responder = SendMessagePurchaseRequestResponder({'message': e.message, 'code': e.code})
            responder.setResponse()
            return responder.getResponse()