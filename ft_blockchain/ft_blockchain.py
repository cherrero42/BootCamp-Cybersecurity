#!/usr/bin/env python
# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    ft_blockchain.py                                   :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cherrero <cherrero@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/05/06 04:27:53 by cherrero          #+#    #+#              #
#    Updated: 2023/05/07 01:23:27 by cherrero         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys
try:
    from flask import Flask, jsonify, request, render_template
    import hashlib
    import json
    import time
except ModuleNotFoundError:
    sys.exit("\nError: Some libraries were not found. Check the requirements.\n")

reward = 1
miner_address = '@my_miner'
target_suffix = '4242'

class Block:
    def __init__(self, index, transactions, previous_hash, timestamp, proof):
        self.index = index
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.proof = proof

    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.current_transactions = []

    def create_genesis_block(self):
        return Block(0, [], "0", time.time(), 0)

    def add_block(self, proof):
        previous_block = self.chain[-1]
        block = Block(len(self.chain), self.current_transactions, previous_block.compute_hash(), time.time(), proof)
        self.chain.append(block)
        self.current_transactions = []
        return block

    def add_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

    def proof_of_work(self, previous_hash, target_suffix):
        proof = 0
        while True:
            hash = hashlib.sha256(f'{previous_hash}{proof}'.encode()).hexdigest()
            if hash.endswith(target_suffix):
                print(hash)
                return proof
            proof += 1

app = Flask(__name__)
blockchain = Blockchain()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    required = ['sender', 'recipient', 'amount']
    if not all(k in values and values[k] for k in required):
        return 'Missing values', 400
    blockchain.add_transaction(values['sender'], values['recipient'], values['amount'])
    return 'Transaction added to block', 200

@app.route('/mine', methods=['GET'])
def mine():
    previous_block = blockchain.chain[-1]
    previous_hash = previous_block.compute_hash()
    proof = blockchain
    proof = blockchain.proof_of_work(previous_hash, target_suffix)
    blockchain.add_transaction('0', miner_address, reward)
    block = blockchain.add_block(proof)
    print(f'Block #{block.index} has been mined. Proof: ', proof)
    response = {
        'message': 'New block mined',
        'index': block.index,
        'transactions': block.transactions,
        'previous_hash': block.previous_hash,
        'timestamp': block.timestamp,
        'proof': block.proof,
    }
    return jsonify(response), 200

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
    'message': 'Full chain',
    'chain': [block.__dict__ for block in blockchain.chain],
    'length': len(blockchain.chain),
    }
    return jsonify(response), 200

@app.route('/waiting', methods=['GET'])
def wait_chain():
    response = {
    'message': 'Waiting mining',
    'waiting': [blockchain.current_transactions],
    'length': len(blockchain.current_transactions),
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)
