from udp import send_packet
from rssi import get_rssi
# from util import update_power_json
import json

class DiscoveryNode:
    def __init__(self, node_id, ip, neighbors, arduino):
        self.node_id = node_id
        self.ip = ip
        self.neighbors = neighbors
        self.arduino = arduino
        self.results = []

    def allowed_neighbors(self):
        return self.neighbors[str(self.node_id)]["allowed_ip"]

    def ip_of(self, node_id):
        return f"192.168.50.{node_id}"

    # ================= START DISCOVERY =================
    def start(self):
        print(f"[NODE {self.node_id}] Start discovery")
        for ip in self.allowed_neighbors():
            pkt = {
                "type": "DISCOVERY",
                "origin": self.node_id,
                "path": [self.node_id],
                "rssi_path": [],
                "sender": self.node_id
            }
            send_packet(ip, pkt)

    # ================= HANDLE DISCOVERY =================
    def handle_discovery(self, msg, sender_ip):
        print(f"[NODE {self.node_id}] RX DISCOVERY from {sender_ip} | {msg}")

        if sender_ip not in self.allowed_neighbors():
            print("[DROP] Not neighbor")
            return

        if self.node_id in msg["path"]:
            print("[DROP] Loop detected")
            return

        rssi = get_rssi(self.arduino)
        new_path = msg["path"] + [self.node_id]
        new_rssi = msg["rssi_path"] + [rssi]

        # cari neighbor selanjutnya
        next_neighbors = []
        for ip in self.allowed_neighbors():
            nid = int(ip.split(".")[-1])
            if nid not in new_path:
                next_neighbors.append(ip)

        # ===== LEAF NODE =====
        if not next_neighbors:
            print(f"[LEAF {self.node_id}] Send RESPONSE")
            response = {
                "type": "RESPONSE",
                "origin": msg["origin"],
                "path": new_path,
                "rssi_path": new_rssi
            }
            prev_node = new_path[-2]
            send_packet(self.ip_of(prev_node), response)
            return

        # ===== FORWARD DISCOVERY =====
        for ip in next_neighbors:
            fwd = {
                "type": "DISCOVERY",
                "origin": msg["origin"],
                "path": new_path,
                "rssi_path": new_rssi,
                "sender": self.node_id
            }
            send_packet(ip, fwd)

    # ================= HANDLE RESPONSE =================
    def handle_response(self, msg):
        print(f"[NODE {self.node_id}] RX RESPONSE | {msg}")

        if self.node_id == msg["origin"]:
            print(f"[NODE {self.node_id}] ✅ FINAL PATH {msg['path']}")
            print(f"[NODE {self.node_id}] ✅ RSSI {msg['rssi_path']}")
            self.results.append(msg)

            # update_power_json(
            #     msg["path"],
            #     msg["rssi_path"]
            # )
            return

        if self.node_id not in msg["path"]:
            return

        idx = msg["path"].index(self.node_id)
        prev_node = msg["path"][idx - 1]
        send_packet(self.ip_of(prev_node), msg)
