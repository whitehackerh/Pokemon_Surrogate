from api.Enums.ResponseCodes import ResponseCodes
from api.Exceptions.CustomExceptions import CustomExceptions
from api.Services.BaseService import BaseService
from api.Models.Listings import Listings

class GetListingsPersonalSummaryService(BaseService):
    def service(self, request):
        try:
            data = {}
            listingsModel = Listings()
            data['count'] = listingsModel.getListingsPersonalRecordsCount(request.get('seller_id'), request.get('status'))
            if data['count'] == 0:
                data['pages'] = 0
            elif data['count'] % 10 == 0:
                data['pages'] = data['count'] // 10
            else:
                data['pages'] = data['count'] // 10 + 1
            return data
        except Exception as e:
            raise CustomExceptions(str(e), ResponseCodes.INTERNAL_SERVER_ERROR)