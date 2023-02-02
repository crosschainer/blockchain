from datetime import datetime
import json
import requests
import os

class MasterNode:
    block_queue = []
    block_storage = None
    network_manager = None

    def __init__(self, block_storage, network_manager):
        self.block_storage = block_storage
        self.network_manager = network_manager

    def calculate_hash(self, index, previous_hash, sender, receiver, amount):
        return sha256(
            f"{index}{previous_hash}{sender}{receiver}{amount}".encode()
        ).hexdigest()

    def create_transaction(self, index, previous_hash, new_hash, sender, receiver, amount):
        data = {
            "index": index,
            "previous_hash": previous_hash,
            "hash": sha256(f"{index}{previous_hash}{sender}{receiver}{amount}".encode()).hexdigest(),
            "sender": sender,
            "receiver": receiver,
            "amount": amount,
            "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }
        self.propose_block(block=data)
       
    def propose_block(self, block):
        self.network_manager.check_peers()
        for peer in self.network_manager.peer_list:
            requests.post(f"{peer}/propose_block", json={"block": block})

    def load_blockchain(self):
        for block in os.listdir(self.block_storage):
            with open(f"{self.block_storage}/{block}") as infile:
                self.block_queue.append(json.loads(infile.read()))

    def validate_block(self, block):
        return (
            block["index"] == len(self.block_storage) + 1
            and block["previous_hash"] == self.block_storage[-1]["hash"]
        )
    
    def start(self):
        self.load_blockchain()
        while True:
            if self.block_queue:
                block = self.block_queue.pop(0)
                if self.validate_block(block):
                    next_block = len(self.block_storage) + 1
                    with open(f"{self.block_storage}/{next_block}.json") as outfile:
                        outfile.write(json.dumps(block))