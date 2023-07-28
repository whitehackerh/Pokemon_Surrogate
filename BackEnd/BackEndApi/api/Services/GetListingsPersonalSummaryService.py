from api.Enums.ResponseCodes import ResponseCodes
from api.Enums.ListingStatus import ListingStatus
from api.Exceptions.CustomExceptions import CustomExceptions
from api.Services.BaseService import BaseService
from api.Models.Listings import Listings

class GetListingsPersonalSummaryService(BaseService):
    def service(self, request):
        try:
            data = {}
            model = Listings()
            seller_id = request.get('seller_id')
            status = request.get('status')
            if status == ListingStatus.SELLING:
                data['count'] = model.getListingsPersonalSellingRecordsCount(seller_id, status)
            elif status == ListingStatus.SOLD:
                data['count'] = model.getListingsPersonalSoldRemovedRecordsCount(seller_id, [status, ListingStatus.REMOVED])
            if data['count'] == 0:
                data['pages'] = 0
            elif data['count'] % 10 == 0:
                data['pages'] = data['count'] // 10
            else:
                data['pages'] = data['count'] // 10 + 1
            return data
        except Exception as e:
            raise CustomExceptions(str(e), ResponseCodes.INTERNAL_SERVER_ERROR)