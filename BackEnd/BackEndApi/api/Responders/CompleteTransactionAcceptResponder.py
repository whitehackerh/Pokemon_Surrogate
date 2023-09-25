from api.Responders.BaseResponder import BaseResponder

class CompleteTransactionAcceptResponder(BaseResponder):
    def __init__(self, exception = None):
        super().__init__('completeTransactionAccept', exception)