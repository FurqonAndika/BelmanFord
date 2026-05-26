import json
from util import build_graph, reconstruct_path

def eebellman_ford(graph, src):
    table = {v: {'cost': float('inf'), 'previous': None} for v in graph}
    table[src]['cost'] = 0

    for _ in range(len(graph) - 1):
        updated = False
        for u in graph:
            for v, w in graph[u]:
                if table[u]['cost'] + w < table[v]['cost']:
                    table[v]['cost'] = table[u]['cost'] + w
                    table[v]['previous'] = u
                    updated = True
        if not updated:
            break

    return table



if __name__ == "__main__":
    graph = build_graph("neighbors.json", "power.json")
    power = json.load(open("power.json"))
    table = eebellman_ford(graph, src="1")
    path = reconstruct_path(table, src="1", dest="15")
    print(path)

    
