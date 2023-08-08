from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from api.Validators.GetPurchaseRequestsValidator import GetPurchaseRequestsValidator
from api.Services.GetPurchaseRequestsService import GetPurchaseRequestsService
from api.Responders.GetPurchaseRequestsResponder import GetPurchaseRequestsResponder
from api.Exceptions.CustomExceptions import CustomExceptions

class GetPurchaseRequestsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            validator = GetPurchaseRequestsValidator(data=request.data)
            validator.is_valid(raise_exception=True)
            service = GetPurchaseRequestsService()
            data = service.service(request.data)
            responder = GetPurchaseRequestsResponder()
            responder.setResponse(data)
            return responder.getResponse()
        except CustomExceptions as e:
            responder = GetPurchaseRequestsResponder({'message': e.message, 'code': e.code})
            responder.setResponse()
            return responder.getResponse()