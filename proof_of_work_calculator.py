# from block import BlockUtils
import hashlib
import logging
import pickle

logging.basicConfig(level=logging.INFO)


class ProofOfWorkCalculator:
    proof_length = 4

    @classmethod
    def set_proof_length(cls, proof_length: int) -> None:
        cls.proof_length = proof_length

    @classmethod
    def calculate_proof_of_work(cls, last_proof: int, block_bytes: bytes) -> int:
        """
        Simple Proof of Work Algorithm:
         - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
         - p is the previous proof, and p' is the new proof
        :param block_bytes:
        :param last_proof: using this to prevent generation of unnecessary blocks
        :return: <int>
        """
        logging.info(f"Calculating the proof_of_work for block: {block_bytes}")
        proof = 0
        while cls.is_valid_proof(last_proof, block_bytes, proof) is False:
            proof += 1
        # print("\n 3113")
        # pickle.dumps(block_bytes)
        # print("\n")
        return proof

    @classmethod
    def is_valid_proof(cls, last_proof: int, block_bytes: bytes, proof: int) -> bool:
        """
        Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?
        :param block_bytes:
        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :return: <bool> True if correct, False if not.
        """
        # print("\n 3114")
        # pickle.dumps(block_bytes)
        # print("\n")
        guess = block_bytes + f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:cls.proof_length] == "0" * cls.proof_length
