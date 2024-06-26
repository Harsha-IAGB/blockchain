import logging
import os
import pickle
import warnings
from block import Block

from google.cloud import pubsub_v1 as gps
from urllib3.exceptions import NotOpenSSLWarning

from blockchain import Blockchain
from constants import GPubSub
from proof_of_work_calculator import ProofOfWorkCalculator

# Filter out the NotOpenSSLWarning
warnings.filterwarnings("ignore", category=NotOpenSSLWarning)


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GPubSub.credentials_file


class Participant:
    def __init__(self):
        self.blockchain = Blockchain()
        self.subscriber = gps.SubscriberClient()
        self.publisher = gps.PublisherClient()
        self.topic = {
            "transaction-add": {
                "topic_path": GPubSub.Topic.TransactionAdd.topic_path,
                "subscription_path": GPubSub.Topic.TransactionAdd.subscription_path,
            },
            "block-add": {
                "topic_path": GPubSub.Topic.BlockAdd.topic_path,
                "subscription_path": GPubSub.Topic.BlockAdd.subscription_path,
                "callback": self.block_add_callback
            }
        }
        self.topic["block-add"]["pull_future"] = self.subscriber.subscribe(
            self.topic["block-add"]["subscription_path"],
            self.topic["block-add"]["callback"]
        )
        with self.subscriber:
            logging.info("Actively listening for requests to add blocks...")
            try:
                self.topic["block-add"]["pull_future"].result()
            except TimeoutError:
                self.topic["block-add"]["pull_future"].cancel()
                self.topic["block-add"]["pull_future"].result()

    def block_add_callback(self, message):
        block = pickle.loads(message.data)
        # print(1991, block.previous_hash, block.index, block.timestamp, block.transactions, block.proof)
        logging.info(f"\nProcessing new block: {block}")
        logging.info(f"Checking previous hash of the block...")
        if self.blockchain.last_block.hash == block.previous_hash:
            logging.info("Hash verified successfully. Checking authenticity of proof of work...")
            if ProofOfWorkCalculator.is_valid_proof(self.blockchain.last_block.proof, block.proof_bytes, block.proof):
                logging.info("Proof of work validated.")
                logging.info("Adding the block to the chain...")
                self.blockchain.add_block(block)
                logging.info(f"State of blockchain:\nblockchain:\n{self.blockchain}\n{self.blockchain.chain}")
            else:
                logging.warning(f"Invalid proof of work for block: {block}")
        else:
            logging.warning(f"Invalid previous hash of block: {block}")
        # message.ack()


if __name__ == '__main__':
    participant = Participant()
