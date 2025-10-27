
import csv
import random

def bellman_ford(graph, src):
    table = {vertex: {'cost': float('inf'), 'previous': None} for vertex in graph}
    table[src]['cost'] = 0

    relaxation = False

    for _ in range(len(graph) - 1):
        relaxation = False
        for u in graph:
            for v, weight in graph[u]:
                if table[u]['cost'] != float('inf') and table[u]['cost'] + weight < table[v]['cost']:
                    table[v]['cost'] = table[u]['cost'] + weight
                    table[v]['previous'] = u
                    relaxation = True
        if not relaxation:
            break

    if relaxation:
        for u in graph:
            for v, weight in graph[u]:
                if table[u]['cost'] != float('inf') and table[u]['cost'] + weight < table[v]['cost']:
                    print("Graph contains a negative weight cycle")
                    return None

    return table


def print_path(table, src, dest):
    path = []
    current = dest
    while current != src and current is not None:
        path.append(current)
        current = table[current]['previous']
    path.append(src)
    path.reverse()
    print(f"Shortest path from {src} to {dest}: {' -> '.join(path)}")


def save_to_csv(table, filename="bellman_ford_result.csv"):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Node", "Cost", "Previous"])
        for vertex, data in table.items():
            writer.writerow([vertex, data['cost'], data['previous']])
    print(f"Hasil disimpan ke file: {filename}")


if __name__ == "__main__":
    # Struktur graph sesuai gambar kamu
    graph_example = {
        'A': [('B', random.uniform(1, 5)), ('C', random.uniform(1, 5)), ('D', random.uniform(1, 5))],
        'B': [('E', random.uniform(1, 5))],
        'C': [('F', random.uniform(1, 5))],
        'D': [('G', random.uniform(1, 5))],
        'E': [('H', random.uniform(1, 5))],
        'F': [('I', random.uniform(1, 5))],
        'G': [('J', random.uniform(1, 5))],
        'H': [('K', random.uniform(1, 5)),('L', random.uniform(1, 5))],
        'I': [('K', random.uniform(1, 5)), ('L', random.uniform(1, 5))],
        'J': [('K', random.uniform(1, 5)), ('L', random.uniform(1, 5))],
        'K': [('M', random.uniform(1, 5))],
        'L': [('N', random.uniform(1, 5))],
        'M': [('O', random.uniform(1, 5))],
        'N': [('O', random.uniform(1, 5))],
        'O': []
    }

    source = 'A'
    result_table = bellman_ford(graph_example, source)

    if result_table:
        for vertex, data in result_table.items():
            print(f"{vertex}: Cost = {data['cost']:.3f}, Previous = {data['previous']}")
        print_path(result_table, source, 'O')
        save_to_csv(result_table)




'''import csv
import random

def bellman_ford(graph, src):
    table = {vertex: {'cost': float('inf'), 'previous': None} for vertex in graph}
    table[src]['cost'] = 0

    relaxation = False

    for _ in range(len(graph) - 1):
        relaxation = False
        for u in graph:
            for v, weight in graph[u]:
                if table[u]['cost'] != float('inf') and table[u]['cost'] + weight < table[v]['cost']:
                    table[v]['cost'] = table[u]['cost'] + weight
                    table[v]['previous'] = u
                    relaxation = True
        if not relaxation:
            break

    if relaxation:
        for u in graph:
            for v, weight in graph[u]:
                if table[u]['cost'] != float('inf') and table[u]['cost'] + weight < table[v]['cost']:
                    print("Graph contains a negative weight cycle")
                    return None

    return table


def reconstruct_path(table, src, dest):
    path = []
    current = dest
    while current != src and current is not None:
        path.append(current)
        current = table[current]['previous']
    if current == src:
        path.append(src)
        path.reverse()
        return path
    else:
        return None


def generate_graph():
    """Bikin graph sesuai gambar dengan bobot random tiap edge."""
    g = {
        'A': [('B', 4), ('C', random.uniform(1, 5)), ('D', random.uniform(1, 5))],
        'B': [('E', random.uniform(1, 5))],
        'C': [('F', random.uniform(1, 5))],
        'D': [('G', random.uniform(1, 5))],
        'E': [('H', random.uniform(1, 5))],
        'F': [('I', random.uniform(1, 5))],
        'G': [('J', random.uniform(1, 5))],
        'H': [('K', random.uniform(1, 5)), ('L', random.uniform(1, 5))],
        'I': [('K', random.uniform(1, 5)), ('L', random.uniform(1, 5))],
        'J': [('K', random.uniform(1, 5)), ('L', random.uniform(1, 5))],
        'K': [('M', random.uniform(1, 5))],
        'L': [('N', random.uniform(1, 5))],
        'M': [('O', random.uniform(1, 5))],
        'N': [('O', random.uniform(1, 5))],
        'O': []
    }
    return g


def save_results_to_csv(all_results, filename="bellman_ford_multiple_runs.csv"):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Run", "Node", "Cost", "Previous", "Path"])
        for run_id, result in enumerate(all_results, start=1):
            table = result['table']
            path = " -> ".join(result['path']) if result['path'] else "No path"
            for node, data in table.items():
                writer.writerow([run_id, node, data['cost'], data['previous'], path])
    print(f"Hasil semua percobaan disimpan ke file: {filename}")


if __name__ == "__main__":
    source = 'A'
    destination = 'O'
    num_runs = 1000  # ubah jumlah percobaan di sini

    all_results = []

    for i in range(num_runs):
        print(f"\n=== Percobaan ke-{i+1} ===")
        graph = generate_graph()
        result_table = bellman_ford(graph, source)
        path = reconstruct_path(result_table, source, destination)

        if result_table and path:
            print(f"Path dari {source} ke {destination}: {' -> '.join(path)}")
            print(f"Total cost = {result_table[destination]['cost']:.4f}")
        else:
            print("Path tidak ditemukan.")

        all_results.append({
            'table': result_table,
            'path': path
        })

    save_results_to_csv(all_results)
'''