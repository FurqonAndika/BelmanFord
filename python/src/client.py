import socket
import time
import datetime

SERVER_IP = "172.16.13.8"   # IP Raspberry Pi (atau 192.168.10.1 jika ad-hoc)
PORT = 9999
LOG_FILE = "client_log.txt"   # Nama file log

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
counter = 0

def log_message(text):
    """Catat pesan ke file log dengan timestamp"""
    with open(LOG_FILE, "a") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {text}\n")

try:
    print(f" Client started, logging to {LOG_FILE}")
    while True:
        try:
            counter += 1
            msg = "1"
            sock.sendto(msg.encode(), (SERVER_IP, PORT))

            sock.settimeout(2)
            try:
                data, _ = sock.recvfrom(1024)
                decoded = data.decode().strip()
                print(f"[{counter:03}] Received:", decoded)
                log_message(f"[{counter:03}] OK  | {decoded}")
            except socket.timeout:
                print(f"[{counter:03}] Timeout, no reply.")
                log_message(f"[{counter:03}] TIMEOUT")

            time.sleep(1)
        except :
            pass
except KeyboardInterrupt:
    print("\n Client stopped by user.")
    log_message("=== Client stopped ===")

finally:
    sock.close()
