import socket
import json

PORT = 5005

def send_packet(ip, data):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(json.dumps(data).encode(), (ip, PORT))
    print(f"[UDP SEND] → {ip}:{PORT} | {data}")
    sock.close()
