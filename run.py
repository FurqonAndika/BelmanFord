import socket
import json
import subprocess
from discovery import DiscoveryNode
from arduino_serial import ArduinoSerialReader

#from util import build_graph, reconstruct_path
import json
# from eeBellmanFord import eebellman_ford

PORT = 5005


def get_ip():
    return subprocess.check_output(["hostname", "-I"]).decode().split()[0]

def run():
    ip = get_ip()
    node_id = int(ip.split(".")[-1])

    neighbors = json.load(open("neighbors.json"))

    arduino = ArduinoSerialReader()
    arduino.connect()

    node = DiscoveryNode(node_id, ip, neighbors, arduino)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", PORT))

    if node_id == 1:
        node.start()

    print(f"[NODE {node_id}] Listening...")

    while True:
        data, addr = sock.recvfrom(4096)
        msg = json.loads(data.decode())

        if msg["type"] == "DISCOVERY":
            node.handle_discovery(msg, addr[0])
        
        elif msg["type"] == "RESPONSE":
            node.handle_response(msg)
            

         

if __name__ == "__main__":
    run()
    # graph = build_graph("neighbors.json", "power.json")
    # table = eebellman_ford(graph, src="1")
    # path = reconstruct_path(table, src="1", dest="4")
    # print("choosen path ",path)

