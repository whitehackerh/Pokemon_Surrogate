from api.Enums.ResponseCodes import ResponseCodes
from api.Exceptions.CustomExceptions import CustomExceptions
from api.Services.BaseService import BaseService
from api.models import Users

class SetUserInfoService(BaseService):
    def service(self, request):
        try:
            model = Users()
            model.setUserInfo(request)
            return None
        except Exception as e:
            raise CustomExceptions(e, ResponseCodes.INTERNAL_SERVER_ERROR)