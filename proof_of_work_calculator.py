import hashlib
import json
import pickle


class ProofOfWorkCalculator:
    proof_length = 4

    @classmethod
    def set_proof_length(cls, proof_length: int) -> None:
        cls.proof_length = proof_length

    @classmethod
    def calculate_proof_of_work(cls, last_proof: int, block_data: dict) -> int:
        """
        Simple Proof of Work Algorithm:
         - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
         - p is the previous proof, and p' is the new proof
        :param block_data:
        :param last_proof: <int>
        :return: <int>
        """
        proof = 0
        block_data_string = pickle.dumps(block_data)
        while cls.is_valid_proof(last_proof, block_data_string, proof) is False:
            proof += 1
        return proof

    @classmethod
    def is_valid_proof(cls, last_proof: int, block_data_bytes: bytes, proof: int) -> bool:
        """
        Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?
        :param block_data_bytes:
        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :return: <bool> True if correct, False if not.
        """
        guess = block_data_bytes + f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0" * cls.proof_length
