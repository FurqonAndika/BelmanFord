import socket
from driver.ArduinoSerial import ArduinoSerialReader  # pastikan file class kamu bernama arduino_reader.py

SERVER_IP = "0.0.0.0"  # listen di semua interface
PORT = 9999

# --- Inisialisasi Arduino Serial ---
arduino = ArduinoSerialReader(baudrate=115200)
if not arduino.connect():
    print(" Gagal konek ke Arduino.")
    exit()

# --- Setup UDP Server ---
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((SERVER_IP, PORT))
print(f"server listening on {SERVER_IP}:{PORT}")

try:
    while True:
        data, addr = sock.recvfrom(1024)
        msg = data.decode().strip()
        print(f"[CLIENT {addr}] Pesan diterima:", msg)

        # --- Baca tegangan dari Arduino ---
        voltage = arduino.read_voltage()

        if voltage is not None:
            reply = str(voltage)
        else:
            reply = "Gagal baca tegangan."

        # --- Kirim balasan ke client ---
        sock.sendto(reply.encode(), addr)
        print(f"[SERVER] Balas ke {addr}: {reply}")

except KeyboardInterrupt:
    print("\n Dihentikan oleh user.")
finally:
    arduino.disconnect()
    sock.close()
