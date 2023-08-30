from api.Responders.BaseResponder import BaseResponder

class SendMessagePurchaseRequestResponder(BaseResponder):
    def __init__(self, exception = None):
        super().__init__('sendMessagePurchaseRequest', exception)