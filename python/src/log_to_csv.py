import csv
import re

INPUT_FILE = "client_log.txt"   # nama file log kamu
OUTPUT_FILE = "client_log.csv"

# Regex untuk deteksi baris OK
pattern = re.compile(r'\[(.*?)\]\s+\[(\d+)\]\s+OK\s+\|\s+([\d.]+)')

rows = []

with open(INPUT_FILE, "r") as f:
    for line in f:
        match = pattern.search(line)
        if match:
            timestamp = match.group(1)
            counter = int(match.group(2))
            voltage = float(match.group(3))
            rows.append([timestamp, counter, voltage])

# Simpan ke CSV
with open(OUTPUT_FILE, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Timestamp", "Counter", "Voltage"])
    writer.writerows(rows)

print(f"✅ Konversi selesai! Total data tersimpan: {len(rows)}")
print(f"📁 File CSV: {OUTPUT_FILE}")
