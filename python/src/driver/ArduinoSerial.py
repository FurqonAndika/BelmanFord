'''
import serial
import threading
import serial.tools.list_ports

class ArduinoSerialReader:
    def __init__(self, baudrate=9600, timeout=1, vid=None, pid=None):
        self.baudrate = baudrate
        self.timeout = timeout
        self.vid = vid
        self.pid = pid
        self.serial_conn = None
        self.running = False
        self.data_callback = None

    def auto_detect_port(self):
        """Scan COM ports and try to find Arduino."""
        ports = serial.tools.list_ports.comports()
        for port in ports:
            # If VID/PID specified, use them
            if self.vid and self.pid:
                if (port.vid == self.vid) and (port.pid == self.pid):
                    return port.device
            else:
                # Otherwise try by name
                if "Arduino" in port.description or "CH340" in port.description:
                    return port.device

        # If nothing matched, just return the first available port
        if ports:
            print("⚠️ No Arduino match found, using first port:", ports[0].device)
            return ports[0].device

        return None

    def connect(self):
        """Auto detect port and open connection."""
        port = self.auto_detect_port()
        if not port:
            print("❌ No COM port detected.")
            return False
        try:
            self.serial_conn = serial.Serial(port, self.baudrate, timeout=self.timeout)
            self.running = True
            print(f"✅ Connected to {port} at {self.baudrate} baud.")
            return True
        except Exception as e:
            print(f"❌ Error opening port {port}: {e}")
            return False

    def disconnect(self):
        self.running = False
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
            print("🔌 Serial connection closed.")

    def start_reading(self, callback=None):
        if callback:
            self.data_callback = callback
        thread = threading.Thread(target=self._read_loop, daemon=True)
        thread.start()

    def _read_loop(self):
        while self.running and self.serial_conn and self.serial_conn.is_open:
            try:
                line = self.serial_conn.readline().decode(errors="ignore").strip()
                if line:
                    if self.data_callback:
                        self.data_callback(line)
                    else:
                        print("Arduino says:", line)
            except Exception as e:
                print("⚠️ Serial read error:", e)
               
'''

import serial
import threading
import serial.tools.list_ports

class ArduinoSerialReader:
    def __init__(self, baudrate=9600, timeout=1, vid=None, pid=None):
        self.baudrate = baudrate
        self.timeout = timeout
        self.vid = vid
        self.pid = pid
        self.serial_conn = None
        self.running = False
        self.data_callback = None

    def auto_detect_port(self):
        """Scan COM ports and try to find Arduino."""
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if self.vid and self.pid:
                if (port.vid == self.vid) and (port.pid == self.pid):
                    return port.device
            else:
                if "Arduino" in port.description or "CH340" in port.description:
                    return port.device

        if ports:
            # print("⚠️ No Arduino match found, using first port:", ports[0].device)
            return ports[0].device

        return None

    def connect(self):
        """Auto detect port and open connection."""
        port = self.auto_detect_port()
        if not port:
            print("❌ No COM port detected.")
            return False
        try:
            self.serial_conn = serial.Serial(port, self.baudrate, timeout=self.timeout)
            self.running = True
            # print(f"✅ Connected to {port} at {self.baudrate} baud.")
            return True
        except Exception as e:
            print(f"❌ Error opening port {port}: {e}")
            return False

    def disconnect(self):
        self.running = False
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
            print("🔌 Serial connection closed.")

    def start_reading(self, callback=None):
        if callback:
            self.data_callback = callback
        thread = threading.Thread(target=self._read_loop, daemon=True)
        thread.start()

    def _read_loop(self):
        """Continuous reading in background thread."""
        while self.running and self.serial_conn and self.serial_conn.is_open:
            try:
                line = self.serial_conn.readline().decode(errors="ignore").strip()
                if line:
                    if self.data_callback:
                        self.data_callback(line)
                    else:
                        print("Arduino says:", line)
            except Exception as e:
                print("⚠️ Serial read error:", e)

    def read_voltage(self):
        """Read one line from Arduino and return as float if possible."""
        if not self.serial_conn or not self.serial_conn.is_open:
            print("❌ Serial not connected.")
            return None

        try:
            line = self.serial_conn.readline().decode(errors="ignore").strip()
            if line:
                try:
                    value = float(line)
                    return value
                except ValueError:
                    print(f"⚠️ Non-numeric data received: {line}")
                    return None
            else:
                return None
        except Exception as e:
            print("⚠️ Error reading voltage:", e)
            return None
