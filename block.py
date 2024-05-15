import base64
from time import time
import hashlib
import json
import logging
import pickle
from typing import List

from transaction import Transaction

logging.basicConfig(level=logging.INFO)


class Block:
    def __init__(self, index=None, previous_hash=None, proof=None, timestamp=time(), transactions=None):
        """
        Creates a new block to which transactions can be added.
        :param index:
        :param previous_hash:
        :param proof:
        :param timestamp:
        :param transactions:
        """
        logging.info("Creating a new block...")
        self.index = index
        self.previous_hash = previous_hash
        self.proof = proof
        self.timestamp = timestamp
        self.transactions: List[Transaction] = transactions if transactions else []
        self.next: Block = None

    @property
    def proof_bytes(self) -> bytes:
        """
        :return: bytes of block data that are used for calculating the proof of work
        """
        return json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": base64.b64encode(pickle.dumps(self.transactions)).decode()
        }).encode()

    @property
    def hash_bytes(self) -> bytes:
        """
        :return: bytes of data that are used to compute the hash of a block
        """
        return json.dumps({
            "previous_hash": self.previous_hash,
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": base64.b64encode(pickle.dumps(self.transactions)).decode(),
            "proof": self.proof
        }).encode()

    @property
    def hash(self) -> str:
        """
        :return: sha256 value of the block
        """
        return hashlib.sha256(self.hash_bytes).hexdigest()


if __name__ == '__main__':
    logging.info("Exporting the genesis block...")
    genesis_block = Block(
        index=0,
        previous_hash=0,
        proof=0
    )
    with open("genesis_block", "wb") as f:
        f.write(pickle.dumps(genesis_block))
