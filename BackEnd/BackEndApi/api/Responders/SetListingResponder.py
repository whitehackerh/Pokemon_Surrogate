from api.Responders.BaseResponder import BaseResponder

class SetListingResponder(BaseResponder):
    def __init__(self, exception = None):
        super().__init__('setListing', exception)