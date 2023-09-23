from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from api.Validators.GetAcceptDetailValidator import GetAcceptDetailValidator
from api.Services.GetAcceptDetailService import GetAcceptDetailService
from api.Responders.GetAcceptDetailResponder import GetAcceptDetailResponder
from api.Exceptions.CustomExceptions import CustomExceptions

class GetAcceptDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            validator = GetAcceptDetailValidator(data=request.data)
            validator.is_valid(raise_exception=True)
            service = GetAcceptDetailService()
            data = service.service(request)
            responder = GetAcceptDetailResponder()
            responder.setResponse(data)
            return responder.getResponse()
        except CustomExceptions as e:
            responder = GetAcceptDetailResponder({'message': e.message, 'code': e.code})
            responder.setResponse()
            return responder.getResponse()