from api.Responders.BaseResponder import BaseResponder

class GetMessagesPurchaseRequestResponder(BaseResponder):
    def __init__(self, exception = None):
        super().__init__('getMessagesPurchaseRequest', exception)