from api.Responders.BaseResponder import BaseResponder

class GetListingsPersonalResponder(BaseResponder):
    def __init__(self, exception = None):
        super().__init__('getListingsPersonal', exception)