from api.Responders.BaseResponder import BaseResponder

class SetRequestResponder(BaseResponder):
    def __init__(self, exception = None):
        super().__init__('setRequest', exception)