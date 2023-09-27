from api.Responders.BaseResponder import BaseResponder

class SetReadMessagesAcceptResponder(BaseResponder):
    def __init__(self, exception = None):
        super().__init__('setReadMessagesAccept', exception)