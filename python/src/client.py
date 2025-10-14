import socket
import time

SERVER_IP = "192.168.137.1"   # IP Raspberry Pi (atau 192.168.10.1 jika ad-hoc)
PORT = 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    while True:
        msg = f"ping {time.time()}"
        sock.sendto(msg.encode(), (SERVER_IP, PORT))

        sock.settimeout(2)
        try:
            data, _ = sock.recvfrom(1024)
            print("[CLIENT] Received:", data.decode())
        except socket.timeout:
            print("[CLIENT] Timeout, no reply.")

        time.sleep(1)

except KeyboardInterrupt:
    print(" Client stopped.")
finally:
    sock.close()
