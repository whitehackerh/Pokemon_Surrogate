import os
import uuid
from django.conf import settings
from django.db import transaction
from api.Enums.ResponseCodes import ResponseCodes
from api.Exceptions.CustomExceptions import CustomExceptions
from api.Services.BaseService import BaseService
from api.Services.Utils.ServiceUtils import ServiceUtils
from api.Models.Listing import Listing
from api.Models.ListingPictures import ListingPictures
from api.Models.Fees import Fees
from api.Enums.Path import Path
from api.Enums.ListingStatus import ListingStatus

class SetListingService(BaseService):
    @transaction.atomic
    def service(self, request):
        try:
            if request.data.get('create'):
                self.__createListing(request)
            else:
                self.__updateListing(request)
            return None
        except Exception as e:
            raise CustomExceptions(str(e), ResponseCodes.INTERNAL_SERVER_ERROR)
    
    def __createListing(self, request):
        ### insert listing
        feesModel = Fees()
        seller_id = request.data.get('seller_id')
        listingParams = {
            'seller_id': seller_id,
            'game_title_id': request.data.get('game_title_id'),
            'category': request.data.get('category'),
            'listing_title': request.data.get('listing_title'),
            'description': request.data.get('description'),
            'price_negotiation': request.data.get('price_negotiation'),
            'price': request.data.get('price'),
            'fee_id': feesModel.getAvailableFee().id,
            'status': ListingStatus.SALE_AVAILABLE
        }
        listingModel = Listing(**listingParams)
        listingModel.save()

        ### insert listing_pictures
        listing_id = listingModel.id
        if not request.FILES:
            listingPicturesParam = {
                'listing_id': listing_id,
                'seller_id': seller_id,
                'path': Path.LOGO,
                'sort_no': 1
            }
            listingPictureModel = ListingPictures(**listingPicturesParam)
            listingPictureModel.save()
            return None
        else:
            ServiceUtils.makeDir(os.path.join(settings.MEDIA_ROOT, Path.LISTING_PICTURE_DIR))
            listingPicturesParams = []
            for index in range(1, 11):
                if f'picture{index}' in request.FILES:
                    ### filename: {listing_id}_{uuid}.png
                    filename = f'{listing_id}_{uuid.uuid4().hex}.png'
                    while any(filename == os.path.basename(listingPicture['path']) for listingPicture in listingPicturesParams):
                        filename = f'{listing_id}_{uuid.uuid4().hex}.png'
                    listingPicturesParams.append({
                        'listing_id': listing_id,
                        'seller_id': seller_id,
                        'path': os.path.join(Path.LISTING_PICTURE_DIR, filename),
                        'sort_no': index
                    })
            ListingPictures.objects.bulk_create([ListingPictures(**listingPicturesParam) for listingPicturesParam in listingPicturesParams])
            for listingPicturesParam in listingPicturesParams:
                with open(os.path.join(settings.MEDIA_ROOT, listingPicturesParam['path']), 'wb') as f:
                    for chunk in request.FILES.get(f"picture{listingPicturesParam['sort_no']}").chunks():
                        f.write(chunk)
            return None
    
    def __updateListing(self, request):
        return None