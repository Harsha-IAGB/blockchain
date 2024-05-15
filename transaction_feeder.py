import os
import logging
import os
import pickle
import time
import warnings
from typing import List

from cryptography.hazmat.primitives import hashes
from google.cloud import pubsub_v1 as gps
from urllib3.exceptions import NotOpenSSLWarning

from constants import GPubSub
from private_keys import PrivateKey
from transaction import Transaction

# Filter out the NotOpenSSLWarning
warnings.filterwarnings("ignore", category=NotOpenSSLWarning)

logging.basicConfig(level=logging.INFO)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GPubSub.credentials_file


def compute_transaction_signature(transaction, private_key):
    logging.info(f"Computing digital signature for transaction: {transaction}")
    return private_key.sign(
        transaction.hash_bytes,
        hashes.SHA256()
    )


transactions: List[Transaction] = []
private_key = PrivateKey()

# transaction = Transaction(tid=0, sender="", recipient="Alice", amount=100)
# transaction.signature = compute_transaction_signature(transaction, private_key.alice)
# transactions.append(transaction)
#
# transaction = Transaction(tid=1, sender="", recipient="Bob", amount=100)
# transaction.signature = compute_transaction_signature(transaction, private_key.bob)
# transactions.append(transaction)
#
# transaction = Transaction(tid=2, sender="", recipient="Charlie", amount=100)
# transaction.signature = compute_transaction_signature(transaction, private_key.charlie)
# transactions.append(transaction)
#
# transaction = Transaction(tid=3, sender="Charlie", recipient="Bob", amount=87)
# transaction.signature = compute_transaction_signature(transaction, private_key.bob)
# transactions.append(transaction)


transaction = Transaction(tid=3, sender="Charlie", recipient="Bob", amount=8998)
transaction.signature = compute_transaction_signature(transaction, private_key.bob)
transactions.append(transaction)

transaction = Transaction(tid=3, sender="Charlie", recipient="Bob", amount=87)
transaction.signature = compute_transaction_signature(transaction, private_key.alice)
transactions.append(transaction)

publisher = gps.PublisherClient()
topic_path = "projects/nomadic-botany-422915-m7/topics/transaction-add"
for trans in transactions:
    time.sleep(10)
    transaction_future = publisher.publish(
        topic_path,
        pickle.dumps(trans)
    )
    logging.info(f"Transaction published with ID: {transaction_future.result()}")
