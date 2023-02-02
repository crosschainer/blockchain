from flask import Flask, request
import requests
from utils.list_helper import *


class WebServer:
    app = None
    network_manager = None
    masternode = None

    def __init__(self, network_manager, masternode):
        self.network_manager = network_manager
        self.app = Flask(__name__)
        self.app.add_url_rule('/', view_func=self.default, methods=['GET'])
        self.app.add_url_rule('/ping', view_func=self.pong, methods=['GET'])
        self.app.add_url_rule(
            '/announce', view_func=self.announce, methods=['POST'])
        self.app.add_url_rule(
            '/peers', view_func=self.get_peers, methods=['GET'])
        self.app.add_url_rule(
            '/propose_block', view_func=self.propose_block, methods=['POST'])
        

    def default(self):
        return 'Hello World'

    def pong(self):
        return 'Pong!'

    def get_peers(self):
        return self.network_manager.peer_list

    def get_latest_block(self):
        return masternode.block_storage[-1]

    def propose_block(self):
        data = request.get_json()
        if "block" in data:
            self.masternode.block_queue.append(data["block"])
            return "Added block to queue."

    def announce(self):
        data = request.get_json()
        if (
            "host" in data
            and requests.get(f"{data['host']}/ping").status_code == 200
            and data["host"] not in self.network_manager.peer_list
        ):
            remote_peers = requests.get(f"{data['host']}/peers").json()
            self.network_manager.add_peer(data["host"])
            self.network_manager.peer_list = merge_two_lists(self.network_manager.peer_list, remote_peers)
            return "Added peer to network."

    def run(self):
        self.app.run(host='0.0.0.0', port=8103)
