from api.Responders.BaseResponder import BaseResponder

class DeliverProductAcceptResponder(BaseResponder):
    def __init__(self, exception = None):
        super().__init__('deliverProductAccept', exception)