# run.py
import json
import subprocess
import os
import socket
from node import DiscoveryNode

PORT = 5005

def get_ip():
    try:
        out = subprocess.check_output(["hostname", "-I"]).decode().strip()
        return out.split()[0]
    except:
        return None

def get_mac():
    path = "/sys/class/net/wlan0/address"
    if os.path.exists(path):
        with open(path) as f:
            return f.read().strip()
    return None

def run_node():
    ip = get_ip()
    mac = get_mac()
    if ip is None or mac is None:
        print("[ERROR] Can't determine IP or MAC. Run on Raspberry Pi with wlan0.")
        return

    node_id = int(ip.split(".")[-1])
    neighbors = json.load(open("neighbors.json"))

    print(f"Starting node {node_id} (IP {ip}, MAC {mac})")
    node = DiscoveryNode(node_id, ip, mac, neighbors)

    # create UDP socket to receive packets on all interfaces
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", PORT))

    # If origin node (1) start discovery
    if node_id == 1:
        node.send_discovery()

    print("Listening for UDP packets...")
    while True:
        data, addr = sock.recvfrom(8192)
        try:
            msg = json.loads(data.decode())
        except:
            continue
        mtype = msg.get("type")
        last_ip = addr[0]

        if mtype == "DISCOVERY":
            # ensure incoming msg has fields, pass last_ip for forward decisions
            node.handle_discovery(msg, last_ip)
        elif mtype == "DISCOVERY_RESPONSE":
            node.handle_response(msg)
        # else ignore unknown types

if __name__ == "__main__":
    run_node()
