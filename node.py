# node.py
import json
import random
from udp import send_packet
from rssi import get_rssi

class DiscoveryNode:
    def __init__(self, node_id, ip, mac, neighbors):
        self.node_id = int(node_id)
        self.ip = ip
        self.mac = mac
        self.neighbors = neighbors           # dict parsed from neighbors.json
        self.seen_requests = set()           # set of (origin, seq) that we've processed
        self.rssi_table = {}                 # for node 1: {node_id: rssi}
        # IP prefix assumption (your network): 192.168.50.X
        self.ip_prefix = ".".join(self.ip.split(".")[:3]) + "."

    def ip_of(self, node_id):
        """Return IP string for node id (assumes fixed subnet 192.168.50.X)."""
        return f"{self.ip_prefix}{int(node_id)}"

    # -------------------------
    # Node 1 calls this to start discovery
    # -------------------------
    def send_discovery(self):
        seq = random.randint(100000, 999999)
        pkt = {
            "type": "DISCOVERY",
            "origin": self.node_id,
            "seq": seq,
            "path": [self.node_id],       # list of node ids
            "rssi_path": [],              # list of RSSI values observed at each hop (A->next, next->next,...)
            "sender_id": self.node_id,
            "sender_mac": self.mac,
            "ttl": len(self.neighbors) + 10  # safe large TTL
        }
        print(f"[{self.node_id}] Sending DISCOVERY seq={seq}")
        # send to direct allowed neighbors
        for nb_ip in self.neighbors[str(self.node_id)]["allowed_ip"]:
            send_packet(nb_ip, pkt)

    # -------------------------
    # Handle incoming DISCOVERY
    # last_ip = ip address of who sent this packet to us (from UDP recv)
    # -------------------------
    def handle_discovery(self, msg, last_ip):
        origin = msg["origin"]
        seq = msg["seq"]
        key = (origin, seq)

        # prevent reprocessing same (origin,seq)
        if key in self.seen_requests:
            return
        # also prevent if we are already in path (loop safety)
        if self.node_id in msg.get("path", []):
            return

        self.seen_requests.add(key)

        # measure RSSI from the sender (sender_mac included in msg)
        sender_mac = msg.get("sender_mac")
        rssi = None
        if sender_mac:
            rssi = get_rssi(sender_mac)    # real RSSI on Raspi
        else:
            rssi = None

        # build new path/rssi_path
        new_path = msg["path"] + [self.node_id]
        new_rssi_path = msg.get("rssi_path", []) + [rssi]

        # decrement ttl
        ttl = msg.get("ttl", 10) - 1

        # If this node is the LAST (leaf) — decide leaf by neighbors: if all neighbors are the node that sent this packet
        allowed = self.neighbors.get(str(self.node_id), {}).get("allowed_ip", [])
        # determine whether there exists a neighbor ip other than last_ip
        forwardable = any(nb != last_ip for nb in allowed)

        # If no forwardable neighbor OR ttl exhausted -> prepare response and send back via reverse path
        if not forwardable or ttl <= 0:
            # This node must send a response back using the recorded path
            response = {
                "type": "DISCOVERY_RESPONSE",
                "origin": origin,
                "seq": seq,
                "path": new_path,        # forward path from origin .. this node
                "rssi_path": new_rssi_path
            }
            print(f"[{self.node_id}] Leaf or TTL=0, sending response back for origin {origin} seq={seq}")
            # send to previous hop in path (reverse)
            if len(new_path) >= 2:
                prev_node = new_path[-2]
                prev_ip = self.ip_of(prev_node)
                send_packet(prev_ip, response)
            else:
                # if no prev (rare) and origin==this node, store directly
                if origin == self.node_id:
                    self._store_response(response)
            return

        # Otherwise forward discovery to neighbors (except the node we got it from)
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

        # send our own partial response to previous hop as well so A can start collecting partials early
        # (optional) — we can also only have leaves reply. We'll still send our own local response to prev.
        response_self = {
            "type": "DISCOVERY_RESPONSE",
            "origin": origin,
            "seq": seq,
            "path": new_path,
            "rssi_path": new_rssi_path
        }
        # reply back to previous hop (if exists)
        if len(new_path) >= 2:
            prev_node = new_path[-2]
            prev_ip = self.ip_of(prev_node)
            send_packet(prev_ip, response_self)

        # forward to other neighbors
        for nb_ip in allowed:
            if nb_ip == last_ip:
                continue
            send_packet(nb_ip, forward_pkt)

    # -------------------------
    # Handle incoming DISCOVERY_RESPONSE
    # This will be forwarded along reverse path until it reaches origin
    # -------------------------
    def handle_response(self, msg):
        origin = msg["origin"]
        seq = msg["seq"]
        path = msg.get("path", [])
        rssi_path = msg.get("rssi_path", [])

        # If this node is the origin for which the response is intended
        if origin == self.node_id:
            # store rssi info for final processing (Bellman-Ford)
            sender = path[-1]
            self.rssi_table[sender] = rssi_path
            print(f"[{self.node_id}] Received final response from node {sender}, rssi_path={rssi_path}")
            return

        # Otherwise forward response to previous node in path (i.e., node with lower index)
        # Find our position in path
        if self.node_id not in path:
            # Not in path? ignore
            return
        idx = path.index(self.node_id)
        if idx == 0:
            # weird: origin is before us, but not equal; ignore
            return
        prev_node = path[idx - 1]
        prev_ip = self.ip_of(prev_node)
        # forward unchanged response
        send_packet(prev_ip, msg)

    # -------------------------
    # internal: store response if origin == self.node_id (fallback)
    # -------------------------
    def _store_response(self, response):
        sender = response["path"][-1]
        self.rssi_table[sender] = response.get("rssi_path", [])
