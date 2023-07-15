from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from api.Validators.GetListingsPersonalSummaryValidator import GetListingsPersonalSummaryValidator
from api.Services.GetListingsPersonalSummaryService import GetListingsPersonalSummaryService
from api.Responders.GetListingsPersonalSummaryResponder import GetListingsPersonalSummaryResponder
from api.Exceptions.CustomExceptions import CustomExceptions

class GetListingsPersonalSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            validator = GetListingsPersonalSummaryValidator(data=request.data)
            validator.is_valid(raise_exception=True)
            service = GetListingsPersonalSummaryService()
            data = service.service(request.data)
            responder = GetListingsPersonalSummaryResponder()
            responder.setResponse(data)
            return responder.getResponse()
        except CustomExceptions as e:
            responder = GetListingsPersonalSummaryResponder({'message': e.message, 'code': e.code})
            responder.setResponse()
            return responder.getResponse()