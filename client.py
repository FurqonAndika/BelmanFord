import socket
import time

HOST = "192.168.10.1"

PORT = 5000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((HOST, PORT))
	while True:
		message ="Hello Raspi "
		s.sendall(message.encode())
		data =s.recv(1024).decode()
		print("received:",data)
		time.sleep(1)


