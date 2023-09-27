from api.Responders.BaseResponder import BaseResponder

class GetMessagesAcceptResponder(BaseResponder):
    def __init__(self, exception = None):
        super().__init__('getMessagesAccept', exception)