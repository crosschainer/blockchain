import requests

class NetworkManager:
    peer_list = []

    def add_peer(self, peer):
        if peer not in self.peer_list:
            self.peer_list.append(peer)

    def remove_peer(self, peer):
        if peer in self.peer_list:
            self.peer_list.remove(peer)

    def check_peers(self):
        for peer in self.peer_list:
            ping = requests.get(f"{peer}/ping")
            if ping.status_code != 200:
                self.remove_peer(peer)

    