import base64
import os
from api.Enums.ListingStatus import ListingStatus

class ServiceUtils:
    def makeDir(path):
        if not os.path.exists(path):
            os.makedirs(path)
    
    def getListingStatus(code):
        if code == ListingStatus.SELLING:
            return 'selling'
        elif code == ListingStatus.IN_PROGRESS:
            return 'in progress'
        elif code == ListingStatus.SOLD:
            return 'sold'
        
    def getBase64FromPath(path):
        with open(path, 'rb') as file:
            return base64.b64encode(file.read()).decode('utf-8')