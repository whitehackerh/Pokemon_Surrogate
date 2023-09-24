from api.Responders.BaseResponder import BaseResponder

class PayForAcceptResponder(BaseResponder):
    def __init__(self, exception = None):
        super().__init__('payForAccept', exception)