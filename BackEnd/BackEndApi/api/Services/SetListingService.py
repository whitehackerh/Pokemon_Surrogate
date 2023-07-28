import os
import uuid
from django.conf import settings
from django.db import transaction
from api.Enums.ResponseCodes import ResponseCodes
from api.Exceptions.CustomExceptions import CustomExceptions
from api.Services.BaseService import BaseService
from api.Services.Utils.ServiceUtils import ServiceUtils
from api.Models.Listings import Listings
from api.Models.ListingPictures import ListingPictures
from api.Models.Fees import Fees
from api.Enums.Path import Path
from api.Enums.ListingStatus import ListingStatus

class SetListingService(BaseService):
    @transaction.atomic
    def service(self, request):
        try:
            if request.data.get('listing_id'):
                self.__updateListing(request)
            else:
                self.__createListing(request)
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
            'status': ListingStatus.SELLING
        }
        listingsModel = Listings(**listingParams)
        listingsModel.save()

        ### insert listing_pictures
        listing_id = listingsModel.id
        if not request.FILES:
            self.__registerDefaultPicture(listing_id, seller_id)
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
        listing_id = request.data.get('listing_id')
        seller_id = request.data.get('seller_id')
        listingModel = Listings()
        if ServiceUtils.isEnableUpdateListing(listing_id, seller_id):
            listingModel.updateListing(request)
            listingPicturesModel = ListingPictures()
            oldListingPictures = listingPicturesModel.getListingPictures(listing_id)
            
            # stash file path
            oldPicturePaths = []
            for oldPicture in oldListingPictures:
                oldPicturePaths.append(oldPicture.path)
            
            listingPicturesModel.deleteListingPictures(listing_id)

            if not request.FILES:
                self.__registerDefaultPicture(listing_id, seller_id)
            else:
                ServiceUtils.makeDir(os.path.join(settings.MEDIA_ROOT, Path.LISTING_PICTURE_DIR))
                listingPicturesParams = []
                pictureNameList = []
                for oldPicture in oldPicturePaths:
                    pictureNameList.append(os.path.basename(oldPicture))
                for index in range(1, 11):
                    if f'picture{index}' in request.FILES:
                        ### filename: {listing_id}_{uuid}.png
                        filename = f'{listing_id}_{uuid.uuid4().hex}.png'
                        while any(filename == pictureName for pictureName in pictureNameList):
                            filename = f'{listing_id}_{uuid.uuid4().hex}.png'
                        listingPicturesParams.append({
                            'listing_id': listing_id,
                            'seller_id': seller_id,
                            'path': os.path.join(Path.LISTING_PICTURE_DIR, filename),
                            'sort_no': index
                        })
                        pictureNameList.append(filename)
                ListingPictures.objects.bulk_create([ListingPictures(**listingPicturesParam) for listingPicturesParam in listingPicturesParams])
                for listingPicturesParam in listingPicturesParams:
                    with open(os.path.join(settings.MEDIA_ROOT, listingPicturesParam['path']), 'wb') as f:
                        for chunk in request.FILES.get(f"picture{listingPicturesParam['sort_no']}").chunks():
                            f.write(chunk)

            # delete old pictures
            for oldPicture in oldPicturePaths:
                targetPath = os.path.join(settings.MEDIA_ROOT, oldPicture)
                if os.path.exists(targetPath) and oldPicture != Path.LOGO:
                    os.remove(targetPath)
        else:
            raise CustomExceptions('Unauthorized Error.', ResponseCodes.INTERNAL_SERVER_ERROR)
        return None
    
    def __registerDefaultPicture(self, listing_id, seller_id):
        listingPicturesParam = {
            'listing_id': listing_id,
            'seller_id': seller_id,
            'path': Path.LOGO,
            'sort_no': 1
        }
        listingPictureModel = ListingPictures(**listingPicturesParam)
        listingPictureModel.save()