import logging
import pickle
from typing import List

from block import Block

logging.basicConfig(level=logging.INFO)


class Blockchain:
    def __init__(self, proof_length=4):
        """
        Initializes a new chain to which blocks can be added.
        :param proof_length:
        """
        logging.info("Creating a new blockchain...")
        self.chain: List[Block] = []
        self.proof_length = proof_length
        logging.info("Adding genesis block...")
        with open("genesis_block", "rb") as f:
            genesis_block = pickle.loads(f.read())
        self.chain.append(genesis_block)

    @property
    def length(self) -> int:
        return len(self.chain)

    @property
    def first_block(self) -> Block:
        return self.chain[0]

    @property
    def last_block(self) -> Block:
        return self.chain[-1]

    def add_block(self, block: Block) -> None:
        logging.info(f"Adding block: {block}")
        self.last_block.next = block
        self.chain.append(block)
        logging.info(f"Block: {block} added to chain: {self}")
