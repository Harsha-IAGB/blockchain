import hashlib
import json
import pickle
from time import time


class BlockUtils:
    class ProofData:
        def __init__(self, index, timestamp, transactions):
            self.index = index
            self.timestamp = timestamp
            self.transactions = transactions

    class HashData:
        def __init__(self, previous_hash, index, timestamp, transactions, proof):
            self.previous_hash = previous_hash
            self.index = index
            self.timestamp = timestamp
            self.transactions = transactions
            self.proof = proof


class Block:
    def __init__(self, **kwargs):
        self.index = kwargs.get("index", None)
        self.previous_hash = kwargs.get("previous_hash", None)
        self.proof = kwargs.get("proof", None)
        self.timestamp = time()
        self.transactions = kwargs.get("transactions", [])

    @property
    def proof_data(self) -> object:
        return BlockUtils.ProofData(
            index=self.index,
            timestamp=self.timestamp,
            transactions=self.transactions
        )

    @property
    def hash_data(self) -> object:
        return BlockUtils.HashData(
            previous_hash=self.previous_hash,
            index=self.index,
            timestamp=self.timestamp,
            transactions=self.transactions,
            proof=self.proof
        )

    @property
    def hash(self) -> str:
        return hashlib.sha256(pickle.dumps(self.hash_data)).hexdigest()
