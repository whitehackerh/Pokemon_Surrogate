from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from api.Validators.GetMessagesPurchaseRequestValidator import GetMessagesPurchaseRequestValidator
from api.Services.GetMessagesPurchaseRequestService import GetMessagesPurchaseRequestService
from api.Responders.GetMessagesPurchaseRequestResponder import GetMessagesPurchaseRequestResponder
from api.Exceptions.CustomExceptions import CustomExceptions

class GetMessagesPurchaseRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            validator = GetMessagesPurchaseRequestValidator(data=request.data)
            validator.is_valid(raise_exception=True)
            service = GetMessagesPurchaseRequestService()
            data = service.service(request.data)
            responder = GetMessagesPurchaseRequestResponder()
            responder.setResponse(data)
            return responder.getResponse()
        except CustomExceptions as e:
            responder = GetMessagesPurchaseRequestResponder({'message': e.message, 'code': e.code})
            responder.setResponse()
            return responder.getResponse()