from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from api.Validators.SetPurchaseRequestValidator import SetPurchaseRequestValidator
from api.Services.SetPurchaseRequestService import SetPurchaseRequestService
from api.Responders.SetPurchaseRequestResponder import SetPurchaseRequestResponder
from api.Exceptions.CustomExceptions import CustomExceptions

class SetPurchaseRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            validator = SetPurchaseRequestValidator(data=request.data)
            validator.is_valid(raise_exception=True)
            service = SetPurchaseRequestService()
            data = service.service(request.data)
            responder = SetPurchaseRequestResponder()
            responder.setResponse(data)
            return responder.getResponse()
        except CustomExceptions as e:
            responder = SetPurchaseRequestResponder({'message': e.message, 'code': e.code})
            responder.setResponse()
            return responder.getResponse()