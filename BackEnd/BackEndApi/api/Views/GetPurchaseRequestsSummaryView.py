from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from api.Validators.GetPurchaseRequestsSummaryValidator import GetPurchaseRequestsSummaryValidator
from api.Services.GetPurchaseRequestsSummaryService import GetPurchaseRequestsSummaryService
from api.Responders.GetPurchaseRequestsSummaryResponder import GetPurchaseRequestsSummaryResponder
from api.Exceptions.CustomExceptions import CustomExceptions

class GetPurchaseRequestsSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            validator = GetPurchaseRequestsSummaryValidator(data=request.data)
            validator.is_valid(raise_exception=True)
            service = GetPurchaseRequestsSummaryService()
            data = service.service(request.data)
            responder = GetPurchaseRequestsSummaryResponder()
            responder.setResponse(data)
            return responder.getResponse()
        except CustomExceptions as e:
            responder = GetPurchaseRequestsSummaryResponder({'message': e.message, 'code': e.code})
            responder.setResponse()
            return responder.getResponse()