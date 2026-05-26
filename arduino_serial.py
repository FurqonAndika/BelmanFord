import serial
import serial.tools.list_ports

class ArduinoSerialReader:
    def __init__(self, baudrate=115200, timeout=1):
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None

    def auto_detect_port(self):
        ports = serial.tools.list_ports.comports()
        for p in ports:
            if "Arduino" in p.description or "CH340" in p.description:
                return p.device
        return ports[0].device if ports else None

    def connect(self):
        port = self.auto_detect_port()
        if not port:
            print("❌ Arduino not found")
            return False
        try:
            self.ser = serial.Serial(port, self.baudrate, timeout=self.timeout)
            print(f"✅ Arduino connected on {port} @ {self.baudrate}")
            return True
        except Exception as e:
            print("❌ Serial error:", e)
            return False

    def read_voltage(self):
        if not self.ser or not self.ser.is_open:
            return None
        try:
            line = self.ser.readline().decode(errors="ignore").strip()
            if line:
                return float(line)
        except:
            pass
        return None
