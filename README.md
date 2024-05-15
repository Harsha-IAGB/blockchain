# Network Security Concepts in Blockchain
## ENPM693 Project

---
# Project Usage
This project relies on GCP's PubSub offering to work and expects a `gcp-pubsub-private-key.json` that can be generated in GCP. Provide this path as a variable in `constants.py`.

This PubSub offering also expects the topics to publish and subscribe to transactions and blocks. These too are specified in the `constants.py` file

Once these constants are setup, the path of private keys of the transaction's recipients need to be specified in `private_keys.py` file. These are loaded at runtime.

With all these constants set up, the code is ready to be executed as follows:
1. start `miner.py` and `participant.py` in 2 separate terminals
2. edit transactions in `transaction_feeder.py` and execute it.
3. post execution, use ^C to exit from the miner and participant sessions.

---
# Block Class

This class represents a block in a blockchain.

## Attributes

- `index`: The index of the block.
- `previous_hash`: The hash of the previous block.
- `proof`: The proof of work for the block.
- `timestamp`: The timestamp of when the block was created.
- `transactions`: A list of transactions in the block.

## Methods

- `proof_bytes() -> bytes`: Returns the bytes of block data used for calculating the proof of work.
- `hash_bytes() -> bytes`: Returns the bytes of data used to compute the hash of a block.
- `hash() -> str`: Returns the SHA256 hash of the block.

## Usage

```python
block = Block(index, previous_hash, proof, timestamp, transactions)
```
---
# Blockchain Class

This class represents a blockchain.

## Attributes

- `chain`: A list containing blocks in the blockchain.
- `proof_length`: The length of proof required for adding new blocks to the chain.

## Methods

- `length() -> int`: Returns the number of blocks in the chain.
- `first_block() -> Block`: Returns the first block in the chain.
- `last_block() -> Block`: Returns the last block in the chain.
- `add_block(block: Block) -> None`: Adds a new block to the chain.

## Usage

```python
blockchain = Blockchain(proof_length)
```

---
# Miner Class

This class represents a miner node in a blockchain network.

## Attributes

- `blockchain`: An instance of the `Blockchain` class representing the blockchain.
- `current_transactions`: A list containing current transactions being processed by the miner.
- `subscriber`: A Google Cloud Pub/Sub subscriber client.
- `publisher`: A Google Cloud Pub/Sub publisher client.
- `topic`: A dictionary containing information about topics for adding transactions and blocks.

## Methods

- `transaction_add_callback(message) -> None`: Callback function for adding transactions received through Pub/Sub.
- `block_add_callback(message) -> None`: Callback function for adding blocks received through Pub/Sub.

## Usage

```python
python miner.py
```

---
# Participant Class

This class represents a participant node in a blockchain network.

## Attributes

- `blockchain`: An instance of the `Blockchain` class representing the blockchain.
- `subscriber`: A Google Cloud Pub/Sub subscriber client.
- `publisher`: A Google Cloud Pub/Sub publisher client.
- `topic`: A dictionary containing information about topics for adding blocks.

## Methods

- `block_add_callback(message) -> None`: Callback function for adding blocks received through Pub/Sub.

## Usage

```python
python participant.py
```