import hashlib
import json
import logging

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes


class Transaction:
    def __init__(self, tid=None, sender=None, recipient=None, amount=None, signature=None):
        self.tid = tid
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.signature = signature

    def __reduce__(self):
        tok = (self.__class__, (self.tid, self.sender, self.recipient, self.amount, self.signature))
        return tok

    @property
    def hash_bytes(self) -> bytes:
        return json.dumps({
            "tid": self.tid,
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount
        }).encode()

    def is_valid_transaction(self, recipient_public_key) -> bool:
        try:
            recipient_public_key.verify(
                self.signature,
                self.hash_bytes,
                hashes.SHA256()
            )
            logging.info(f"Valid Transaction: {self}")
            return True
        except InvalidSignature:
            logging.warning("Invalid Transaction.")
            return False
