import copy
import time
from typing import List

from block import Block
from blockchain import Blockchain
from concurrent.futures import TimeoutError
from constants import GPubSub, BlockParameters
from google.cloud import pubsub_v1 as gps
from private_keys import PrivateKey
from proof_of_work_calculator import ProofOfWorkCalculator
from urllib3.exceptions import NotOpenSSLWarning
import logging
import os
import pickle

from transaction import Transaction

import warnings

# Filter out the NotOpenSSLWarning
warnings.filterwarnings("ignore", category=NotOpenSSLWarning)


# logging.basicConfig(filename='blockchain.log', level=logging.INFO)
logging.basicConfig(level=logging.INFO)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GPubSub.credentials_file

private_key = PrivateKey()
public_key = {
    "Alice": private_key.alice.public_key(),
    "Bob": private_key.bob.public_key(),
    "Charlie": private_key.charlie.public_key(),
}

class Miner:
    def __init__(self):
        logging.info("Initiating a new miner session...")
        self.blockchain = Blockchain()
        self.current_transactions: List[Transaction] = []
        logging.info("Creating a subscriber client for the miner...")
        self.subscriber = gps.SubscriberClient()
        logging.info("Creating a publisher client for the miner...")
        self.publisher = gps.PublisherClient()
        self.topic = {
            "transaction-add": {
                "topic_path": GPubSub.Topic.TransactionAdd.topic_path,
                "subscription_path": GPubSub.Topic.TransactionAdd.subscription_path,
                "callback": self.transaction_add_callback
            },
            "block-add": {
                "topic_path": GPubSub.Topic.BlockAdd.topic_path,
                "subscription_path": GPubSub.Topic.BlockAdd.subscription_path,
                "callback": self.block_add_callback
            }
        }
        self.topic["transaction-add"]["pull_future"] = self.subscriber.subscribe(
            self.topic["transaction-add"]["subscription_path"],
            self.topic["transaction-add"]["callback"]
        )
        self.topic["block-add"]["pull_future"] = self.subscriber.subscribe(
            self.topic["block-add"]["subscription_path"],
            self.topic["block-add"]["callback"]
        )
        with self.subscriber:
            logging.info("Actively listening for requests to add transactions...")
            logging.info("Actively listening for requests to add blocks...")
            try:
                self.topic["transaction-add"]["pull_future"].result()
                self.topic["block-add"]["pull_future"].result()
            except TimeoutError:
                self.topic["transaction-add"]["pull_future"].cancel()
                self.topic["block-add"]["pull_future"].cancel()
                self.topic["transaction-add"]["pull_future"].result()
                self.topic["block-add"]["pull_future"].result()

    def transaction_add_callback(self, message):
        transaction = pickle.loads(message.data)
        logging.info(f"\nProcessing new transaction: {transaction}")
        logging.info(f"Verifying recipient's digital signature for transaction: {transaction}")
        if transaction.is_valid_transaction(recipient_public_key=public_key[transaction.recipient]):
            logging.info("Recipient digital signature validated.")
            if transaction.sender != "":
                logging.info(f"Checking if sender '{transaction.sender}' has enough balance...")
                sender_balance = 0
                current_block = self.blockchain.first_block
                while current_block is not None:
                    for ledger_transaction in current_block.transactions:
                        if ledger_transaction.recipient == transaction.sender:
                            sender_balance += ledger_transaction.amount
                    current_block = current_block.next
                for unbilled_transaction in self.current_transactions:
                    if unbilled_transaction.recipient == transaction.sender:
                        sender_balance += unbilled_transaction.amount
                logging.info(f"Available sender balance: {sender_balance}. Requested amount: {transaction.amount}")
                if sender_balance >= transaction.amount:
                    pass
                else:
                    logging.warning(f"Insufficient funds for sender: {transaction.sender}")
                    message.ack()
                    return
            logging.info(f"Transaction approved. Adding transaction to the current list...")
            self.current_transactions.append(transaction)
            if len(self.current_transactions) >= BlockParameters.max_transactions:
                logging.info("Max transactions for the block reached. Adding block to the chain")
                block = Block(
                    index=len(self.blockchain.chain),
                    previous_hash=self.blockchain.last_block.hash,
                    transactions = self.current_transactions
                )
                block.proof = ProofOfWorkCalculator.calculate_proof_of_work(self.blockchain.last_block.proof,
                                                                            block.proof_bytes)
                logging.info(f"Publishing block: {block}")
                self.publisher.publish(
                    self.topic["block-add"]["topic_path"],
                    pickle.dumps(block)
                )
        else:
            logging.warning(f"Digital Signature verification failed for transaction: {transaction}."
                            f" Discarding the transaction...")
        message.ack()

    def block_add_callback(self, message):
        block = pickle.loads(message.data)
        print(1991, block.previous_hash, block.index, block.timestamp, block.transactions, block.proof)
        logging.info(f"\nProcessing new block: {block}")
        logging.info(f"Checking previous hash of the block...")
        if self.blockchain.last_block.hash == block.previous_hash:
            logging.info("Hash verified successfully. Checking authenticity of proof of work...")
            if ProofOfWorkCalculator.is_valid_proof(self.blockchain.last_block.proof, block.proof_bytes, block.proof):
                logging.info("Proof of work validated.")
                logging.info("Adding the block to the chain...")
                self.blockchain.add_block(block)
                logging.info("Clearing current transactions...")
                for bt in block.transactions:
                    for ct in self.current_transactions:
                        if bt.tid == ct.tid:
                            self.current_transactions.remove(ct)
                            break
                # current_tids = set()
                # for transaction in block.transactions:
                #     current_tids.add(transaction.tid)
                # for transaction in self.current_transactions:
                #     if transaction.tid in current_tids:
                #         self.current_transactions.remove(transaction)
                logging.info(f"State of blockchain:\nblockchain:\n{self.blockchain}\n{self.blockchain.chain}")
            else:
                logging.warning(f"Invalid proof of work for block: {block}")
        else:
            logging.warning(f"Invalid previous hash of block: {block}")
        message.ack()


# subscriber = gps.SubscriberClient()
# ta_subscription_path = "projects/nomadic-botany-422915-m7/subscriptions/transaction-add"
# ba_subscription_path = "projects/nomadic-botany-422915-m7/subscriptions/block-add-sub"
#
#
# def ta_callback(message):
#     print(message.attributes)
#     print(dir(message))
#     # publisher = gps.PublisherClient()
#     # ba_topic_path = "projects/nomadic-botany-422915-m7/topics/block-add"
#     # ba_data = "baa harsha is a good boy".encode()
#     # ba_future = publisher.publish(ba_topic_path, ba_data)
#     # print(ba_future.result())
#     message.ack()
#
#
# ta_streaming_pull_future = subscriber.subscribe(ta_subscription_path, ta_callback)
# ba_streaming_pull_future = subscriber.subscribe(ba_subscription_path, ta_callback)
#
# with subscriber:
#     try:
#         ta_streaming_pull_future.result()
#         ba_streaming_pull_future.result()
#     except TimeoutError:
#         ta_streaming_pull_future.cancel()
#         ta_streaming_pull_future.result()
#         ba_streaming_pull_future.cancel()
#         ba_streaming_pull_future.result()
#
# def subscribe_transaction_add(self):
#     self.miner.subscribe("transaction/add")
#     try:
#         logging.info("in t/a loop")
#         self.miner.loop_forever()
#     except Exception as ex:
#         logging.error(f"exception occurred:\n{ex}")
#
#
# def subscribe_block_add(self):
#     self.miner.subscribe("block/add")
#     try:
#         logging.info("in b/a loop")
#         self.miner.loop_forever()
#     except Exception as ex:
#         logging.error(f"exception occurred:\n{ex}")
#
#
# print("I am free")

if __name__ == '__main__':
    miner = Miner()
