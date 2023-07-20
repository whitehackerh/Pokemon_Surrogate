import os
from django.conf import settings
from api.Enums.ResponseCodes import ResponseCodes
from api.Exceptions.CustomExceptions import CustomExceptions
from api.Services.BaseService import BaseService
from api.Services.Utils.ServiceUtils import ServiceUtils
from api.Models.Listings import Listings
from api.Models.ListingPictures import ListingPictures
from api.Enums.ListingStatus import ListingStatus

class GetListingDetailService(BaseService):
    def service(self, request):
        try:
            data = {}
            listing_id = request.get('listing_id')
            user_id = request.get('user_id')
            listingsModel = Listings()
            listingPicturesModel = ListingPictures()
            listings = listingsModel.getListingDetail(listing_id)
            listingPictures = listingPicturesModel.getListingPictures(listing_id)
            if listings.count() == 1:
                data = self.__formatResponseData(int(user_id), listing_id, listings[0], listingPictures)
            else:
                data = None
            return data
        except Exception as e:
            raise CustomExceptions(str(e), ResponseCodes.INTERNAL_SERVER_ERROR)
        
    def __formatResponseData(self, user_id, listing_id, listings, listingPictures):
        data = {}
        data['listing_id'] = listing_id
        data['seller_id'] = listings.seller_id
        data['sellers_profile_picture'] = ServiceUtils.getBase64FromPath(os.path.join(settings.MEDIA_ROOT, listings.sellers_profile_picture))
        data['nickname'] = listings.nickname
        data['status'] = listings.status
        data['edit_available'] = data['seller_id'] == user_id and data['status'] == ListingStatus.SELLING
        data['enable_purchase'] = data['seller_id'] != user_id and data['status'] == ListingStatus.SELLING
        data['gane_title_id'] = listings.game_title_id
        data['game_title'] = listings.game_title
        data['category_id'] = listings.category
        data['category'] = ServiceUtils.getListingCategory(data['category_id'])
        data['listing_title'] = listings.listing_title
        data['description'] = listings.description
        data['price_negotiation'] = listings.price_negotiation
        data['price'] = listings.price
        data['pictures'] = []
        for listingPicture in listingPictures:
            data['pictures'].append(ServiceUtils.getBase64FromPath(os.path.join(settings.MEDIA_ROOT, listingPicture.path)))
        return data