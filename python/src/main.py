from driver.ArduinoSerial import ArduinoSerialReader

# def handle_data(line):
#     print("Received:", line)

# arduino = ArduinoSerialReader(baudrate=9600)
# if arduino.connect():
#     arduino.start_reading(callback=handle_data)
#     input("Press Enter to stop...\n")
#     arduino.disconnect()


arduino = ArduinoSerialReader(baudrate=115200)

# if arduino.connect():
#     voltage = arduino.read_voltage()
#     if voltage is not None:
#         print("Tegangan terbaca:", voltage, "V")
#     else:
#         print("Tidak ada data valid.")

arduino.connect()
voltage = arduino.read_voltage()
print(arduino.read_voltage())
for i in range(100):
    print(arduino.read_voltage())
print("done")

# # client.py
# import socket
# import time

# SERVER_IP = "192.168.137.1"   # IP server (ganti IP Pi kalau Pi jadi server)
# PORT = 9999

# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# while True:
#     msg = f"1 {time.time()}"
#     s.sendto(msg.encode(), (SERVER_IP, PORT))
#     data, _ = s.recvfrom(1024)
#     print("[CLIENT] Received:", data.decode())
#     time.sleep(1)