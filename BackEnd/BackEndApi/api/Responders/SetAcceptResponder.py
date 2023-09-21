from api.Responders.BaseResponder import BaseResponder

class SetAcceptResponder(BaseResponder):
    def __init__(self, exception = None):
        super().__init__('setAccept', exception)