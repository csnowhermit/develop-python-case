#!/usr/bin/python26
# encoding=utf-8

import hashlib
import json
from textwrap import dedent
from time import time
from urllib.parse import urlparse
from uuid import uuid4

import requests
from flask import Flask, jsonify, request

"""
区块链类：用于管理链条，存储交易，加入新块等
http://mp.weixin.qq.com/s?__biz=MjM5Nzk2MDU5NA==&mid=2652550970&idx=1&sn=f53181cc240626579bfd53d5c04c038c&chksm=bd3c19c78a4b90d1e1f542ed6ca5c2bf338b6e36eae090e5b2fc1ce83f628f5c99e7eef8315f&scene=0#rd
"""


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.nodes = set()
        self.current_transactions = []
        self.new_block(previous_hash=1, proof=100)

    def register_node(self, address):
        """
        添加新节点到节点链表中
        :param address: 节点地址，eg：http://192.168.100.101:5000/
        :return:
        """
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def valid_chain(self, chain):
        """
        确定一个给定的区块链是有效的
        :param chain: 给定的区块链
        :return:
        """
        last_block = chain[0]
        current_index = 1
        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")
            if block['previous_hash'] != self.hash(last_block):
                return False
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False
            last_block = block
            current_index += 1
        return True

    def resolve_conflicts(self):
        """
        共识算法，解决区块链冲突，使用网络中最长的链
        遍历所有的邻居节点，并用上一个方法检查链的有效性，如果发现有效更长链，就替换掉自己的链。
        :return:
        """
        neighbours = self.nodes
        new_chain = None
        max_length = len(self.nodes)
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain
        if new_chain:
            self.chain = new_chain
            return True
        return False

    def new_block(self, proof, previous_hash=None):
        """
        构建新块并加入到区块链中
        :param proof: <int> 工作量
        :param previous_hash: <str> 前置块的hash值
        :return:
        """
        pass

    def new_transaction(self, sender, recipient, amount):
        """
        将新事务添加到事务列表中
        :param sender: <str> sender的地址
        :param recipient: <str> 收件人的地址
        :param amount: <int> 数量
        :return: 返回下一个带挖掘的块的索引
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })

        return self.last_block['index'] + 1

    @staticmethod
    def __hash__(block):
        """
        静态方法：生成SHA256 hash值
        :param block:
        :return:
        """
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        """
        属性：区块链最后一个块
        :return:
        """
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        """
        简单的工作量证明：查找一个p1，使得hash(pp1)以4个0开头
        p是上一个块的证明，p1是当前的证明
        :param: <int>
        :return: <int>
        """
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        验证：hash(last_proof, proof)是否以4个0开头
        :param: <int> 上一块
        :param: <int> 当前块
        :return:
        """
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()

        return guess_hash[:4] == "0000"


app = Flask(__name__)

node_identifier = str(uuid4()).replace('-', '')

blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1
    )
    block = blockchain.new_block(proof)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }

    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    required = ['sender', 'recipient', 'amount']

    if not all(k in values for k in required):
        return 'Missing values', 400

    # 创建新的交易
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()
    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400
    for node in nodes:
        blockchain.register_node(node)
    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()
    if replaced:
        response = {
            'message': "Our chain was replaced",
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': "Out chain is authoritative",
            'chain': blockchain.chain
        }
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
