from rest_framework.views import APIView
from api.Validators.GetGameTitlesValidator import GetGameTitlesValidator
from api.Services.GetGameTitlesService import GetGameTitlesService
from api.Responders.GetGameTitlesResponder import GetGameTitlesResponder
from api.Exceptions.CustomExceptions import CustomExceptions

class GetGameTitlesView(APIView):
    permission_classes = []

    def get(self, request):
        try:
            GetGameTitlesValidator()
            service = GetGameTitlesService()
            data = service.service()
            responder = GetGameTitlesResponder()
            responder.setResponse(data)
            return responder.getResponse()
        except CustomExceptions as e:
            responder = GetGameTitlesResponder({'message': e.message, 'code': e.code})
            responder.setResponse()
            return responder.getResponse()