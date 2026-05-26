def get_rssi(arduino):
    value = arduino.read_voltage()
    print(f"[RSSI READ] Voltage={value}")
    return value
