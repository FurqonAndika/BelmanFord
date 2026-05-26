import json
import random
from udp import send_packet

MAX_TTL_MARGIN = 5


class DiscoveryNode:
    def __init__(self, node_id, ip, mac, neighbors):
        self.node_id = int(node_id)
        self.ip = ip
        self.mac = mac
        self.neighbors = neighbors

        # FIX: seen berdasarkan (origin, seq, previous_hop)
        self.seen_requests = set()

        # hanya dipakai di node origin (node 1)
        self.rssi_table = {}

        self.id_to_ip = self._build_id_ip_map()
        self.total_nodes = len(self.neighbors)

    # -------------------------
    # Utility
    # -------------------------
    def _build_id_ip_map(self):
        id_ip = {}
        for nid in self.neighbors.keys():
            id_ip[int(nid)] = f"192.168.50.{nid}"
        return id_ip

    def ip_of(self, node_id):
        return self.id_to_ip.get(int(node_id))

    # -------------------------
    # Node 1 memulai discovery
    # -------------------------
    def send_discovery(self):
        seq = random.randint(100000, 999999)

        pkt = {
            "type": "DISCOVERY",
            "origin": self.node_id,
            "seq": seq,
            "path": [self.node_id],
            "rssi_path": [],
            "sender_id": self.node_id,
            "sender_mac": self.mac,
            "ttl": self.total_nodes + MAX_TTL_MARGIN
        }

        print(f"[{self.node_id}] START DISCOVERY seq={seq}")

        for nb_ip in self.neighbors[str(self.node_id)]["allowed_ip"]:
            send_packet(nb_ip, pkt)

    # -------------------------
    # Handle DISCOVERY
    # -------------------------
    def handle_discovery(self, msg, last_ip, rssi):
        print(msg)
        origin = msg["origin"]
        seq = msg["seq"]
        path = msg["path"]
        ttl = msg["ttl"]

        prev_hop = path[-1]
        key = (origin, seq, prev_hop)

        # Cegah proses discovery yang sama lewat hop yang sama
        if key in self.seen_requests:
            return
        self.seen_requests.add(key)

        # Loop protection
        if self.node_id in path:
            return

        # Update path
        new_path = path + [self.node_id]
        new_rssi_path = msg.get("rssi_path", []) + [rssi]
        ttl -= 1

        # Cari neighbor yang valid untuk diteruskan
        candidates = []
        for ip in self.neighbors[str(self.node_id)]["allowed_ip"]:
            if ip == last_ip:
                continue
            nid = int(ip.split(".")[-1])
            if nid in new_path:
                continue
            candidates.append((nid, ip))

        # -------------------------
        # LEAF NODE → KIRIM RESPONSE
        # -------------------------
        if not candidates or ttl <= 0:
            response = {
                "type": "DISCOVERY_RESPONSE",
                "origin": origin,
                "seq": seq,
                "path": new_path,
                "rssi_path": new_rssi_path
            }

            print(f"[{self.node_id}] LEAF → RESPONSE path={new_path}")

            prev_node = new_path[-2]
            send_packet(self.ip_of(prev_node), response)
            return

        # -------------------------
        # FORWARD DISCOVERY
        # -------------------------
        forward_pkt = {
            "type": "DISCOVERY",
            "origin": origin,
            "seq": seq,
            "path": new_path,
            "rssi_path": new_rssi_path,
            "sender_id": self.node_id,
            "sender_mac": self.mac,
            "ttl": ttl
        }

        for nid, ip in candidates:
            send_packet(ip, forward_pkt)

    # -------------------------
    # Handle RESPONSE
    # -------------------------
    def handle_response(self, msg):
        print(msg)
        origin = msg["origin"]
        path = msg["path"]
        rssi_path = msg["rssi_path"]

        # Jika sampai di node origin
        if self.node_id == origin:
            leaf = path[-1]
            self.rssi_table[tuple(path)] = rssi_path
            print(f"[{self.node_id}] FINAL PATH {path} RSSI={rssi_path}")
            return

        # Forward ke node sebelumnya
        idx = path.index(self.node_id)
        prev_node = path[idx - 1]
        send_packet(self.ip_of(prev_node), msg)
