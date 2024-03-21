class Transaction:
    def __init__(self, **kwargs):
        self.sender = kwargs.get("sender", None)
        self.recipient = kwargs.get("recipient", None)
        self.amount = kwargs.get("amount", None)
