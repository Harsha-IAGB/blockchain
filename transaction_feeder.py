import logging
import os
import pickle
import time
from typing import List

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from google.cloud import pubsub_v1 as gps
from urllib3.exceptions import NotOpenSSLWarning

from constants import GPubSub
from private_keys import PrivateKey
from transaction import Transaction
import logging

import warnings

# Filter out the NotOpenSSLWarning
warnings.filterwarnings("ignore", category=NotOpenSSLWarning)

logging.basicConfig(level=logging.INFO)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GPubSub.credentials_file


# private_key = {}
# # Import private key from file
# with open("private_key_alice.pem", "rb") as f:
#     private_key_pem = f.read()
#     private_key["Alice"] = serialization.load_pem_private_key(
#         private_key_pem,
#         password=None,  # No password
#         backend=default_backend()
#     )
# with open("private_key_bob.pem", "rb") as f:
#     private_key_pem = f.read()
#     private_key["Bob"] = serialization.load_pem_private_key(
#         private_key_pem,
#         password=None,  # No password
#         backend=default_backend()
#     )
# with open("private_key_charlie.pem", "rb") as f:
#     private_key_pem = f.read()
#     private_key["Charlie"] = serialization.load_pem_private_key(
#         private_key_pem,
#         password=None,  # No password
#         backend=default_backend()
#     )


def compute_transaction_signature(transaction, private_key):
    logging.info(f"Computing digital signature for transaction: {transaction}")
    return private_key.sign(
        transaction.hash_bytes,
        hashes.SHA256()
    )


transactions: List[Transaction] = []
private_key = PrivateKey()

transaction = Transaction(tid=0, sender="", recipient="Alice", amount=100)
transaction.signature = compute_transaction_signature(transaction, private_key.alice)
transactions.append(transaction)

transaction = Transaction(tid=1, sender="", recipient="Bob", amount=100)
transaction.signature = compute_transaction_signature(transaction, private_key.bob)
transactions.append(transaction)

transaction = Transaction(tid=2, sender="", recipient="Charlie", amount=100)
transaction.signature = compute_transaction_signature(transaction, private_key.charlie)
transactions.append(transaction)

transaction = Transaction(tid=3, sender="Charlie", recipient="Bob", amount=87)
transaction.signature = compute_transaction_signature(transaction, private_key.bob)
transactions.append(transaction)

# transaction = Transaction(tid=4, sender="Bob", recipient="Alice", amount=56)
# transaction.signature = compute_transaction_signature(transaction, private_key.bob)
# transactions.append(transaction)

# transaction = Transaction(tid=5, sender="Alice", recipient="Bob", amount=233)
# transaction.signature = compute_transaction_signature(transaction, private_key.bob)
# transactions.append(transaction)

# transaction = Transaction(tid=6, sender="Alice", recipient="Charlie", amount=33)
# transaction.signature = compute_transaction_signature(transaction, private_key.charlie)
# transactions.append(transaction)
#
# transaction = Transaction(tid=7, sender="Alice", recipient="Bob", amount=23)
# transaction.signature = compute_transaction_signature(transaction, private_key.bob)
# transactions.append(transaction)
#
#
# transaction = Transaction(tid=8, sender="Bob", recipient="Charlie", amount=11)
# transaction.signature = compute_transaction_signature(transaction, private_key.charlie)
# transactions.append(transaction)


publisher = gps.PublisherClient()
topic_path = "projects/nomadic-botany-422915-m7/topics/transaction-add"
for trans in transactions:
    time.sleep(10)
    transaction_future = publisher.publish(
        topic_path,
        pickle.dumps(trans)
    )
    logging.info(f"Transaction published with ID: {transaction_future.result()}")
    # break
