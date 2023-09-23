from api.Responders.BaseResponder import BaseResponder

class GetAcceptDetailResponder(BaseResponder):
    def __init__(self, exception = None):
        super().__init__('getAcceptDetail', exception)