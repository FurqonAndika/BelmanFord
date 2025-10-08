from driver.ArduinoSerial import ArduinoSerialReader

def handle_data(line):
    print("Received:", line)

arduino = ArduinoSerialReader(baudrate=9600)
if arduino.connect():
    arduino.start_reading(callback=handle_data)
    input("Press Enter to stop...\n")
    arduino.disconnect()
