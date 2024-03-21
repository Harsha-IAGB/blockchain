from block import Block
from proof_of_work_calculator import ProofOfWorkCalculator
from transaction import Transaction
from time import time
import hashlib
import pickle


class Blockchain:
    def __init__(self, **kwargs):
        self.chain = []
        self.current_transactions = []
        self.proof_length = kwargs.get("proof_length", 4)
        self.add_block(
            previous_hash='1',
            block=self.new_block(),
            proof=100
        )

    @property
    def last_block(self) -> Block:
        return self.chain[-1]

    def new_block(self) -> Block:
        return Block(
            index=len(self.chain) + 1,
            timestamp=time(),
            transactions=self.current_transactions,
        )

    def add_block(self, previous_hash: str, block: Block, proof: int) -> None:
        block.previous_hash = previous_hash
        block.proof = proof
        self.chain.append(block)
        # Reset the current list of transactions
        self.current_transactions = []

    def add_new_transaction(self, sender, recipient, amount):
        self.current_transactions.append(
            Transaction(
                sender=sender,
                recipient=recipient,
                amount=amount
            )
        )
        return self.last_block.index + 1


if __name__ == '__main__':
    # Example usage
    blockchain = Blockchain()

    blockchain.add_new_transaction("Alice", "Bob", 1)
    blockchain.add_new_transaction("Bob", "Charlie", 2)

    previous_hash = blockchain.last_block.hash
    # Initiating a new block
    block = blockchain.new_block()
    last_proof = blockchain.last_block.proof
    proof = ProofOfWorkCalculator.calculate_proof_of_work(last_proof, block.proof_data)
    # Adding the new block to the chain
    blockchain.add_block(previous_hash, block, proof)
    print("Blockchain:", blockchain.chain)
