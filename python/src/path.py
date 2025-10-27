'''
# comparation
import matplotlib.pyplot as plt

# --- Definisi node dan path ---
nodes_order = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O']

# Path hasil dua algoritma
pure_bellman_path = ['A', 'D', 'G', 'J', 'L', 'N', 'O']
custom_bellman_path = ['A', 'B', 'E', 'H', 'K', 'M', 'O']

# --- Konversi node ke indeks numerik untuk sumbu Y ---
node_to_num = {node: i+1 for i, node in enumerate(nodes_order)}
pure_y = [node_to_num[n] for n in pure_bellman_path]
custom_y = [node_to_num[n] for n in custom_bellman_path]
steps = list(range(1, len(pure_bellman_path)+1))

# --- Plot ---
plt.figure(figsize=(8,5))
plt.plot(steps, pure_y, 'b-s', linestyle='--', label='BF')
plt.plot(steps, custom_y, 'r-s', linestyle='--', label='EEBF')

# --- Label dan gaya ---
plt.title("Path Comparison: EEBF vs BF", fontsize=13, fontweight='bold')
plt.xlabel("Step")
plt.ylabel("Node (Numeric Order)")
plt.yticks(range(1, len(nodes_order)+1), nodes_order)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.show()
'''

import matplotlib.pyplot as plt

# Data path tiap iterasi
paths = [
    ["A", "B", "E", "H", "K", "M", "O"],
    ["A", "C", "F", "I", "L", "N", "O"],
    ["A", "D", "G", "J", "K", "M", "O"],
    ["A", "B", "E", "H", "L", "N", "O"],
    ["A", "C", "F", "I", "K", "M", "O"],
    ["A", "D", "G", "J", "L", "N", "O"]
]

# Mapping node ke angka biar bisa digambar di sumbu Y
nodes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O']
node_y = {n: i for i, n in enumerate(nodes)}

plt.figure(figsize=(10,6))

# Gambar tiap path
for i, path in enumerate(paths, start=1):
    y = [node_y[n] for n in path]
    x = list(range(1, len(path)+1))
    plt.plot(x, y, marker='o', label=f"Iterasi {i}")

# Format sumbu
plt.yticks(range(len(nodes)), nodes)
plt.xticks(range(1, 8), [f"Step {i}" for i in range(1, 8)])
plt.xlabel("Step")
plt.ylabel("Node")
plt.title("Visualisasi Jalur EEBF per Iterasi")
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.show()
