from api.Responders.BaseResponder import BaseResponder

class RemoveListingResponder(BaseResponder):
    def __init__(self, exception = None):
        super().__init__('removeListing', exception)