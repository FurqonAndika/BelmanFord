import csv

def bellman_ford(graph, src):
    # --- Inisialisasi tabel cost dan previous ---
    table = {vertex: {'cost': float('inf'), 'previous': None} for vertex in graph}
    table[src]['cost'] = 0

    # --- Relaxasi |V|-1 kali ---
    for _ in range(len(graph) - 1):
        updated = False
        for u in graph:
            for v, weight in graph[u]:
                if table[u]['cost'] + weight < table[v]['cost']:
                    table[v]['cost'] = table[u]['cost'] + weight
                    table[v]['previous'] = u
                    updated = True
        if not updated:
            break

    return table


def reconstruct_path(table, src, dest):
    """Bangun path dari src ke dest berdasarkan tabel previous."""
    path = []
    current = dest
    while current != src and current is not None:
        path.append(current)
        current = table[current]['previous']
    if current == src:
        path.append(src)
        path.reverse()
        return path
    return None


def run_iterations(graph, src, dest, n_iter=1000, voltage_drop=0.00003496503497*64, filename="BF64.csv"):
    # Inisialisasi tegangan awal
    voltages = {node: 4.2 for node in graph}

    # Jalankan Bellman-Ford sekali (path tetap)
    table = bellman_ford(graph, src)
    path = reconstruct_path(table, src, dest)
    path_str = " -> ".join(path) if path else "No path"

    # Siapkan header CSV
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        header = ["Iterasi", "Path", "Total Energi (V)"] + list(graph.keys())
        writer.writerow(header)

        # Iterasi simulasi
        for i in range(1, n_iter + 1):
            # Kurangi tegangan node yang dilewati
            for node in path:
                voltages[node] -= voltage_drop

            # Hitung total energi di sepanjang path
            total_energy = sum(voltages[node] for node in path)

            # Tulis baris CSV
            row = [i, path_str, total_energy] + [voltages[node] for node in graph.keys()]
            writer.writerow(row)

    print(f"✅ Simulasi selesai. Hasil disimpan ke file: {filename}")


# --- Program utama ---
if __name__ == "__main__":
    graph_example = {
        'A': [('B', 4), ('C', 2), ('D', 3)],
        'B': [('E', 4)],
        'C': [('F', 3)],
        'D': [('G', 5)],
        'E': [('H', 3)],
        'F': [('I', 5)],
        'G': [('J', 2)],
        'H': [('K', 1), ('L', 6)],
        'I': [('K', 2), ('L', 6)],
        'J': [('K', 7), ('L', 1)],
        'K': [('M', 2)],
        'L': [('N', 1)],
        'M': [('O', 3)],
        'N': [('O', 4)],
        'O': []
    }

    run_iterations(graph_example, src='A', dest='O', n_iter=1000)
