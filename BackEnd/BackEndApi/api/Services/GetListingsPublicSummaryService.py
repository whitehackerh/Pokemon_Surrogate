from api.Enums.ResponseCodes import ResponseCodes
from api.Exceptions.CustomExceptions import CustomExceptions
from api.Services.BaseService import BaseService
from api.Models.Listings import Listings

class GetListingsPublicSummaryService(BaseService):
    def service(self):
        try:
            data = {}
            listingsModel = Listings()
            data['count'] = listingsModel.getListingsPublicRecordsCount()
            if data['count'] == 0:
                data['pages'] = 0
            elif data['count'] % 10 == 0:
                data['pages'] = data['count'] // 10
            else:
                data['pages'] = data['count'] // 10 + 1
            return data
        except Exception as e:
            raise CustomExceptions(str(e), ResponseCodes.INTERNAL_SERVER_ERROR)