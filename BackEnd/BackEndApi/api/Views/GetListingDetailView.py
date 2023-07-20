from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from api.Validators.GetListingDetailValidator import GetListingDetailValidator
from api.Services.GetListingDetailService import GetListingDetailService
from api.Responders.GetListingDetailResponder import GetListingDetailResponder
from api.Exceptions.CustomExceptions import CustomExceptions

class GetListingDetailView(APIView):
    permission_classes = []

    def post(self, request):
        try:
            validator = GetListingDetailValidator(data=request.data)
            validator.is_valid(raise_exception=True)
            service = GetListingDetailService()
            data = service.service(request.data)
            responder = GetListingDetailResponder()
            responder.setResponse(data)
            return responder.getResponse()
        except CustomExceptions as e:
            responder = GetListingDetailResponder({'message': e.message, 'code': e.code})
            responder.setResponse()
            return responder.getResponse()