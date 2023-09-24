from api.Responders.BaseResponder import BaseResponder

class RequestPriceAcceptResponder(BaseResponder):
    def __init__(self, exception = None):
        super().__init__('requestPriceAccept', exception)