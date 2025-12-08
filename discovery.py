import time
import json
from udp import broadcast, send_packet
from rssi import get_rssi

class DiscoveryNode:
    def __init__(self, node_id, ip, mac, neighbors):
        self.node_id = node_id
        self.ip = ip
        self.mac = mac
        self.neighbors = neighbors
        self.rssi_table = {}

    def send_discovery(self):
        data = {
            "type": "DISCOVERY",
            "origin": self.node_id,
            "sender": self.node_id,
            "mac": self.mac
        }
        print("[DISCOVERY] Broadcast…")
        broadcast(data)

    def handle_discovery_request(self, msg, addr):
        sender_ip = addr[0]
        sender_mac = msg["mac"]
        sender_id = msg["sender"]

        rssi = get_rssi(sender_mac)

        response = {
            "type": "DISCOVERY_RESPONSE",
            "origin": msg["origin"],
            "from": self.node_id,
            "to": msg["origin"],
            "rssi": rssi,
            "via": self.node_id
        }

        # forward only along allowed neighbors
        if sender_ip in self.neighbors[str(self.node_id)]["allowed_ip"]:
            send_packet(sender_ip, response)

        # also forward to my own neighbors
        for n_ip in self.neighbors[str(self.node_id)]["allowed_ip"]:
            send_packet(n_ip, response)

    def handle_discovery_response(self, msg):
        origin = msg["origin"]
        if origin != self.node_id:
            return

        sender = msg["from"]
        rssi = msg["rssi"]
        self.rssi_table[sender] = rssi
        print(f"[DISCOVERY] Got RSSI from node {sender}: {rssi} dBm")
