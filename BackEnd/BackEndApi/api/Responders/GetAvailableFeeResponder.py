from api.Responders.BaseResponder import BaseResponder

class GetAvailableFeeResponder(BaseResponder):
    def __init__(self, exception = None):
        super().__init__('getAvailableFee', exception)