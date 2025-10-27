import socket
import datetime
from driver.ArduinoSerial import ArduinoSerialReader  # pastikan path benar

SERVER_IP = "0.0.0.0"   # listen di semua interface
PORT = 9999
LOG_FILE = "server_log.txt"

# --- Inisialisasi Arduino Serial ---
arduino = ArduinoSerialReader(baudrate=115200)
if not arduino.connect():
    print("Gagal konek ke Arduino.")
    exit()

# --- Setup UDP Server ---
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((SERVER_IP, PORT))
print(f"Server listening on {SERVER_IP}:{PORT}")

counter = 0

def log_message(text):
    """Catat pesan ke file log dengan timestamp"""
    with open(LOG_FILE, "a") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {text}\n")

try:
    while True:
        data, addr = sock.recvfrom(1024)
        msg = data.decode().strip()
        counter += 1

        print(f"\n[{counter:03}] [CLIENT {addr}] Pesan diterima: {msg}")
        log_message(f"[{counter:03}] FROM {addr} | Pesan: {msg}")

        # --- Baca tegangan dari Arduino ---
        voltage = arduino.read_voltage()
        if voltage is not None:
            reply = f"{voltage:.2f} V"
        else:
            reply = "Gagal baca tegangan."

        # --- Kirim balasan ke client ---
        sock.sendto(reply.encode(), addr)
        print(f"[SERVER] Balas ke {addr}: {reply}")

        # --- Catat juga ke log ---
        log_message(f"[{counter:03}] TO {addr} | Tegangan: {reply}")

except KeyboardInterrupt:
    print("\n Server dihentikan oleh user.")
    log_message("=== Server stopped ===")

finally:
    arduino.disconnect()
    sock.close()
    print("🔌 Koneksi ditutup.")
