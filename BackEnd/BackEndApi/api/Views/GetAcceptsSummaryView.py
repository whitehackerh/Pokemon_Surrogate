from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from api.Validators.GetAcceptsSummaryValidator import GetAcceptsSummaryValidator
from api.Services.GetAcceptsSummaryService import GetAcceptsSummaryService
from api.Responders.GetAcceptsSummaryResponder import GetAcceptsSummaryResponder
from api.Exceptions.CustomExceptions import CustomExceptions

class GetAcceptsSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            validator = GetAcceptsSummaryValidator(data=request.data)
            validator.is_valid(raise_exception=True)
            service = GetAcceptsSummaryService()
            data = service.service(request)
            responder = GetAcceptsSummaryResponder()
            responder.setResponse(data)
            return responder.getResponse()
        except CustomExceptions as e:
            responder = GetAcceptsSummaryResponder({'message': e.message, 'code': e.code})
            responder.setResponse()
            return responder.getResponse()