from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from api.Validators.RemoveListingValidator import RemoveListingValidator
from api.Services.RemoveListingService import RemoveListingService
from api.Responders.RemoveListingResponder import RemoveListingResponder
from api.Exceptions.CustomExceptions import CustomExceptions

class RemoveListingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            validator = RemoveListingValidator(data=request.data)
            validator.is_valid(raise_exception=True)
            service = RemoveListingService()
            data = service.service(request.data)
            responder = RemoveListingResponder()
            responder.setResponse(data)
            return responder.getResponse()
        except CustomExceptions as e:
            responder = RemoveListingResponder({'message': e.message, 'code': e.code})
            responder.setResponse()
            return responder.getResponse()