from api.Responders.BaseResponder import BaseResponder

class GetAcceptsResponder(BaseResponder):
    def __init__(self, exception = None):
        super().__init__('getAccepts', exception)