from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from api.Validators.SetReadMessagesPurchaseRequestValidator import SetReadMessagesPurchaseRequestValidator
from api.Services.SetReadMessagesPurchaseRequestService import SetReadMessagesPurchaseRequestService
from api.Responders.SetReadMessagesPurchaseRequestResponder import SetReadMessagesPurchaseRequestResponder
from api.Exceptions.CustomExceptions import CustomExceptions

class SetReadMessagesPurchaseRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            validator = SetReadMessagesPurchaseRequestValidator(data=request.data)
            validator.is_valid(raise_exception=True)
            service = SetReadMessagesPurchaseRequestService()
            data = service.service(request.data)
            responder = SetReadMessagesPurchaseRequestResponder()
            responder.setResponse(data)
            return responder.getResponse()
        except CustomExceptions as e:
            responder = SetReadMessagesPurchaseRequestResponder({'message': e.message, 'code': e.code})
            responder.setResponse()
            return responder.getResponse()