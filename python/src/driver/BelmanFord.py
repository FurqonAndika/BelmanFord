def bellman_ford(graph, src):
    # Step 1: Initialize costs and previous nodes in a single dictionary
    table = {vertex: {'cost': float('inf'), 'previous': None} for vertex in graph}
    table[src]['cost'] = 0

    relaxation = False  # Flag to track if any updates occur in this iteration

    # Step 2: Relax edges |V| - 1 times, with early stopping using relaxation flag
    for i in range(len(graph) - 1):
        for u in graph:
            for v, weight in graph[u]:
                if table[u]['cost'] != float('inf') and table[u]['cost'] + weight < table[v]['cost']:
                    table[v]['cost'] = table[u]['cost'] + weight
                    table[v]['previous'] = u
                    relaxation = True
        # If no updates were made, we can break early
        if not relaxation:
            break

    # Step 3: Check for negative-weight cycles only if updates occurred
    if relaxation:  # Only check for negative cycles if relaxation occurred
        for u in graph:
            for v, weight in graph[u]:
                if table[u]['cost'] != float('inf') and table[u]['cost'] + weight < table[v]['cost']:
                    print("Graph contains a negative weight cycle")
                    return None

    return table


def print_table(table):
    print("Table of costs and previous nodes:")
    for vertex, data in table.items():
        print(f"{vertex}: Cost = {data['cost']}, Previous = {data['previous']}")


def print_path(table, src, dest):
    path = []
    current = dest
    while current != src:
        path.append(current)
        current = table[current]['previous']
    path.append(src)
    path.reverse()
    print(f"Shortest path from {src} to {dest}: {' -> '.join(path)}")


if __name__ == "__main__":
    
    # Example graph
    graph_example = {
        'A': [('F', 3), ('B', 2), ('D', 5)],
        'B': [('E', 1)],
        'C': [('B', 7), ('G', 4)],
        'D': [('E', 1)],
        'E': [('C', -3), ('G', 3)],
        'F': [('B', -4)],
        'G': [('D', -1)],

    }

    # Compute the shortest paths from source vertex 'A'
    source = 'A'


    output_table = bellman_ford(graph_example, source)
    if output_table:
        print_table(output_table)
        # Example: Print the shortest path from A to G
        print_path(output_table, source, 'G')

    else:
        print("No valid shortest path table generated due to negative weight cycle.") 