from api.Responders.BaseResponder import BaseResponder

class DeleteMessagePurchaseRequestResponder(BaseResponder):
    def __init__(self, exception = None):
        super().__init__('deleteMessagePurchaseRequest', exception)