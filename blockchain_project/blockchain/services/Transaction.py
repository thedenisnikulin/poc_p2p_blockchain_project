class Transaction:
    def __init__(self, sender, recipient, amount: int):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount

    @property
    def serialized(self) -> dict:
        return {
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': self.amount
        }