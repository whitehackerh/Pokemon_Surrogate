import os
from django.conf import settings
from api.Enums.ResponseCodes import ResponseCodes
from api.Enums.ListingStatus import ListingStatus
from api.Exceptions.CustomExceptions import CustomExceptions
from api.Services.BaseService import BaseService
from api.Services.Utils.ServiceUtils import ServiceUtils
from api.Models.Listings import Listings

class GetListingsPersonalService(BaseService):
    def service(self, request):
        try:
            data = {}
            seller_id = request.get('seller_id')
            status = request.get('status')
            model = Listings()
            page = request.get('page')
            limit = 10
            offset = 0
            if page > 1:
                # 10 records / page
                offset = ((page - 1) * limit)
            records = None
            if status == ListingStatus.SELLING:
                records = model.getListingsPersonalSelling(seller_id, status, offset, limit)
            elif status == ListingStatus.SOLD:
                records = model.getListingsPersonalSoldRemoved(seller_id, [status, ListingStatus.REMOVED], offset, limit)
            if not records:
                data['listings'] = []
                return data
            data = self.__formatResponseData(records)
            return data
        except Exception as e:
            raise CustomExceptions(str(e), ResponseCodes.INTERNAL_SERVER_ERROR)
        
    def __formatResponseData(self, records):
        data = {}
        data['listings'] = []
        for record in records:
            listing = {}
            listing['picture'] = ServiceUtils.getBase64FromPath(os.path.join(settings.MEDIA_ROOT, record.path))
            listing['listing_id'] = record.id
            listing['listing_title'] = record.listing_title
            listing['game_title'] = record.game_title
            listing['price'] = record.price
            data['listings'].append(listing)
        return data