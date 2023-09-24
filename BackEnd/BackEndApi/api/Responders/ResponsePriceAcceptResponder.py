from api.Responders.BaseResponder import BaseResponder

class ResponsePriceAcceptResponder(BaseResponder):
    def __init__(self, exception = None):
        super().__init__('responsePriceAccept', exception)