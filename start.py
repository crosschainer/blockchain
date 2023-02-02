from api.webserver import WebServer
from node.masternode import MasterNode
from network import NetworkManager

network_manager = NetworkManager()
masternode = MasterNode(network_manager=network_manager, block_storage="blocks")
webserver = WebServer(network_manager=network_manager, masternode=masternode)

def main():
    masternode.start()
    webserver.run()

if __name__ == '__main__':
    main()
