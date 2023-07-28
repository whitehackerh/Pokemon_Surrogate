from rest_framework.views import APIView
from api.Validators.GetListingsPublicSummaryValidator import GetListingsPublicSummaryValidator
from api.Services.GetListingsPublicSummaryService import GetListingsPublicSummaryService
from api.Responders.GetListingsPublicSummaryResponder import GetListingsPublicSummaryResponder
from api.Exceptions.CustomExceptions import CustomExceptions

class GetListingsPublicSummaryView(APIView):
    permission_classes = []

    def post(self, request):
        try:
            GetListingsPublicSummaryValidator()
            service = GetListingsPublicSummaryService()
            data = service.service()
            responder = GetListingsPublicSummaryResponder()
            responder.setResponse(data)
            return responder.getResponse()
        except CustomExceptions as e:
            responder = GetListingsPublicSummaryResponder({'message': e.message, 'code': e.code})
            responder.setResponse()
            return responder.getResponse()