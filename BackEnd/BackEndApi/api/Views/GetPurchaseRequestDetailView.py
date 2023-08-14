from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from api.Validators.GetPurchaseRequestDetailValidator import GetPurchaseRequestDetailValidator
from api.Services.GetPurchaseRequestDetailService import GetPurchaseRequestDetailService
from api.Responders.GetPurchaseRequestDetailResponder import GetPurchaseRequestDetailResponder
from api.Exceptions.CustomExceptions import CustomExceptions

class GetPurchaseRequestDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            validator = GetPurchaseRequestDetailValidator(data=request.data)
            validator.is_valid(raise_exception=True)
            service = GetPurchaseRequestDetailService()
            data = service.service(request.data)
            responder = GetPurchaseRequestDetailResponder()
            responder.setResponse(data)
            return responder.getResponse()
        except CustomExceptions as e:
            responder = GetPurchaseRequestDetailResponder({'message': e.message, 'code': e.code})
            responder.setResponse()
            return responder.getResponse()