from api.Responders.BaseResponder import BaseResponder

class GetListingsPublicResponder(BaseResponder):
    def __init__(self, exception = None):
        super().__init__('getListingsPublic', exception)