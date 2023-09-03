from api.Responders.BaseResponder import BaseResponder

class SetReadMessagesPurchaseRequestResponder(BaseResponder):
    def __init__(self, exception = None):
        super().__init__('setReadMessagesPurchaseRequest', exception)