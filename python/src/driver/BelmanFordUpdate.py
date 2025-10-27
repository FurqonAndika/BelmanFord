import csv
import math

V_DROP = 0.00003496503497*64 
INITIAL_VOLTAGE = 4.2
ITERATIONS = 1000

# === Graph Definition ===
graph = {
    'A': [('B', 4.2), ('C', 4.2), ('D', 4.2)],
    'B': [('E', 4.2)],
    'C': [('F', 4.2)],
    'D': [('G', 4.2)],
    'E': [('H', 4.2)],
    'F': [('I', 4.2)],
    'G': [('J', 4.2)],
    'H': [('K', 4.2),('L', 4.2)],
    'I': [('K', 4.2), ('L', 4.2)],
    'J': [('K', 4.2), ('L', 4.2)],
    'K': [('M', 4.2)],
    'L': [('N', 4.2)],
    'M': [('O', 4.2)],
    'N': [('O', 4.2)],
    'O': []
}


def bellman_ford_max(graph, src, voltages):
    """Versi Bellman-Ford untuk mencari energi maksimum"""
    table = {vertex: {'energy': -math.inf, 'previous': None} for vertex in graph}
    table[src]['energy'] = voltages[src]

    for _ in range(len(graph) - 1):
        for u in graph:
            for v, _ in graph[u]:
                if table[u]['energy'] + voltages[v] > table[v]['energy']:
                    table[v]['energy'] = table[u]['energy'] + voltages[v]
                    table[v]['previous'] = u

    return table


def get_path(table, src, dest):
    path = []
    current = dest
    while current != src and current is not None:
        path.append(current)
        current = table[current]['previous']
    path.append(src)
    path.reverse()
    return path


# === MAIN SIMULATION ===
voltages = {node: INITIAL_VOLTAGE for node in graph}

with open("bellman_energi64.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    header = ["Iterasi", "Path", "Total Energi (V)"] + list(graph.keys())
    writer.writerow(header)

    for i in range(1, ITERATIONS + 1):
        table = bellman_ford_max(graph, 'A', voltages)
        path = get_path(table, 'A', 'O')

        # Total energi di path
        total_energy = sum(voltages[n] for n in path)

        # Kurangi energi node yang dilewati
        for n in path:
            voltages[n] -= V_DROP

        # Simpan ke CSV
        row = [i, " -> ".join(path), round(total_energy, 6)] + [round(voltages[n], 6) for n in graph]
        writer.writerow(row)

        print(f"Iterasi {i}: {' -> '.join(path)} | Total Energi = {total_energy:.6f} V")

print("\n✅ Selesai. File disimpan sebagai 'bellman_energ.csv'")
