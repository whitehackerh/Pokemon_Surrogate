from rest_framework.views import APIView
from api.Validators.GetRequestsSummaryValidator import GetRequestsSummaryValidator
from api.Services.GetRequestsSummaryService import GetRequestsSummaryService
from api.Responders.GetRequestsSummaryResponder import GetRequestsSummaryResponder
from api.Exceptions.CustomExceptions import CustomExceptions

class GetRequestsSummaryView(APIView):
    permission_classes = []

    def post(self, request):
        try:
            validator = GetRequestsSummaryValidator(data=request.data)
            validator.is_valid(raise_exception=True)
            service = GetRequestsSummaryService()
            data = service.service(request)
            responder = GetRequestsSummaryResponder()
            responder.setResponse(data)
            return responder.getResponse()
        except CustomExceptions as e:
            responder = GetRequestsSummaryResponder({'message': e.message, 'code': e.code})
            responder.setResponse()
            return responder.getResponse()