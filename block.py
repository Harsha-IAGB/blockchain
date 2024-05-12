import base64
from time import time
import hashlib
import json
import logging
import pickle
from typing import List

from transaction import Transaction

logging.basicConfig(level=logging.INFO)


# class BlockUtils:
#     class ProofData:
#         def __init__(self, index, timestamp, transactions):
#             self.index = index
#             self.timestamp = timestamp
#             self.transactions = transactions
#
#         # def __reduce__(self):
#         #     tok = (self.__class__, (self.index, self.timestamp, self.transactions))
#         #     return tok
#
#     class HashData:
#         def  __init__(self, previous_hash, index, timestamp, transactions, proof):
#             self.previous_hash = previous_hash
#             self.index = index
#             self.timestamp = timestamp
#             self.transactions = transactions
#             self.proof = proof
#
#         # def __reduce__(self):
#         #     tok = (self.__class__, (self.previous_hash, self.index, self.timestamp, self.transactions, self.proof))
#         #     return tok


class Block:
    def __init__(self, index=None, previous_hash=None, proof=None, timestamp=time(), transactions=None):
        logging.info("Creating a new block...")
        self.index = index
        self.previous_hash = previous_hash
        self.proof = proof
        self.timestamp = timestamp
        self.transactions: List[Transaction] = transactions if transactions else []
        self.next: Block = None

    @property
    def proof_bytes(self) -> bytes:
        return json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": base64.b64encode(pickle.dumps(self.transactions)).decode()
        }).encode()

    @property
    def hash_bytes(self) -> bytes:
        return json.dumps({
            "previous_hash": self.previous_hash,
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": base64.b64encode(pickle.dumps(self.transactions)).decode(),
            "proof": self.proof
        }).encode()

    @property
    def hash(self) -> str:
        return hashlib.sha256(self.hash_bytes).hexdigest()

    # def __reduce__(self):
    #     tok = (self.__class__, (self.index, self.previous_hash, self.proof, self.transactions))
    #     return tok


if __name__ == '__main__':
    logging.info("Exporting the genesis block...")
    genesis_block = Block(
        index=0,
        previous_hash=0,
        proof=0
    )
    with open("genesis_block", "wb") as f:
        f.write(pickle.dumps(genesis_block))
