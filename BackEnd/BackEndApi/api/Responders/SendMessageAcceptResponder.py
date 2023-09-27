from api.Responders.BaseResponder import BaseResponder

class SendMessageAcceptResponder(BaseResponder):
    def __init__(self, exception = None):
        super().__init__('sendMessageAccept', exception)