from api.Responders.BaseResponder import BaseResponder

class GetListingDetailResponder(BaseResponder):
    def __init__(self, exception = None):
        super().__init__('getListingDetail', exception)