from api.Responders.BaseResponder import BaseResponder

class GetRequestDetailResponder(BaseResponder):
    def __init__(self, exception = None):
        super().__init__('getRequestDetail', exception)