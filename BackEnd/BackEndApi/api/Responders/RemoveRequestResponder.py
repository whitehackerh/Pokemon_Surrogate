from api.Responders.BaseResponder import BaseResponder

class RemoveRequestResponder(BaseResponder):
    def __init__(self, exception = None):
        super().__init__('removeRequest', exception)