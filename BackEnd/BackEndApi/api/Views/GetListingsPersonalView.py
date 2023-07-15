from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from api.Validators.GetListingsPersonalValidator import GetListingsPersonalValidator
from api.Services.GetListingsPersonalService import GetListingsPersonalService
from api.Responders.GetListingsPersonalResponder import GetListingsPersonalResponder
from api.Exceptions.CustomExceptions import CustomExceptions

class GetListingsPersonalView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            validator = GetListingsPersonalValidator(data=request.data)
            validator.is_valid(raise_exception=True)
            service = GetListingsPersonalService()
            data = service.service(request.data)
            responder = GetListingsPersonalResponder()
            responder.setResponse(data)
            return responder.getResponse()
        except CustomExceptions as e:
            responder = GetListingsPersonalResponder({'message': e.message, 'code': e.code})
            responder.setResponse()
            return responder.getResponse()