from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from api.Validators.SetListingValidator import SetListingValidator
from api.Services.SetListingService import SetListingService
from api.Responders.SetListingResponder import SetListingResponder
from api.Exceptions.CustomExceptions import CustomExceptions

class SetListingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            validator = SetListingValidator(data=request.data)
            validator.is_valid(raise_exception=True)
            service = SetListingService()
            data = service.service(request)
            responder = SetListingResponder()
            responder.setResponse(data)
            return responder.getResponse()
        except CustomExceptions as e:
            responder = SetListingResponder({'message': e.message, 'code': e.code})
            responder.setResponse()
            return responder.getResponse()