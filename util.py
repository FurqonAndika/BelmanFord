import json
import os

POWER_FILE = "power.json"

def update_power_json(path, rssi_path):
    """
    Update power.json based on discovery response
    path       : [1, 3, 6, 9, 11]
    rssi_path  : [r13, r36, r69, r911]
    """

    if not os.path.exists(POWER_FILE):
        print("[POWER] ❌ power.json not found")
        return

    with open(POWER_FILE, "r") as f:
        power_data = json.load(f)

    for i in range(1, len(path)):
        node_id = str(path[i])          # node tujuan hop
        rssi = rssi_path[i - 1]
        if rssi==None:rssi=0

        if node_id in power_data:
            power_data[node_id]["power"] = rssi
            print(f"[POWER] 🔄 Node {node_id} ← RSSI {rssi}")

    with open(POWER_FILE, "w") as f:
        json.dump(power_data, f, indent=2)

'''

def build_graph(neighbors_file, power_file):
    neighbors = json.load(open(neighbors_file))
    power = json.load(open(power_file))

    graph = {nid: [] for nid in neighbors}

    for u, u_info in neighbors.items():
        for v, v_info in neighbors.items():
            if u == v:
                continue

            # jika IP u ada di allowed_ip v → u bisa kirim ke v
            u_ip = f"192.168.50.{u}"
            if u_ip in v_info["allowed_ip"]:
                weight = power[v]["power"]   # NEGATIVE POWER
                graph[u].append((v, weight))

    return graph
'''

def build_graph(neighbors_file, power_file):
    neighbors = json.load(open(neighbors_file))
    power = json.load(open(power_file))

    MAX_POWER = 5.0
    graph = {nid: [] for nid in neighbors}

    for u in neighbors:
        for v in neighbors:
            if u == v:
                continue

            if f"192.168.50.{u}" in neighbors[v]["allowed_ip"]:
                weight = MAX_POWER - power[v]["power"]
                graph[u].append((v, weight))

    return graph


def reconstruct_path(table, src, dest):
    path = []
    current = dest
    visited = set()

    while current and current not in visited:
        visited.add(current)
        path.append(current)
        if current == src:
            break
        current = table[current]['previous']

    if path[-1] != src:
        return None

    return path[::-1]
