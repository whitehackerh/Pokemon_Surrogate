from api.Enums.ResponseCodes import ResponseCodes
from api.Exceptions.CustomExceptions import CustomExceptions
from api.Services.BaseService import BaseService
from api.Models.Fees import Fees

class GetAvailableFeeService(BaseService):
    def service(self):
        try:
            data = {}
            model = Fees()
            record = model.getAvailableFee()
            data = self.__formatResponseData(record)
            return data
        except Exception as e:
            raise CustomExceptions(str(e), ResponseCodes.INTERNAL_SERVER_ERROR)
        
    def __formatResponseData(self, record):
        return {
            'id': record.id,
            'percentage': record.percentage
        }