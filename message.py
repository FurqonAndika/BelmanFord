import json

def make_discovery(origin, seq, ttl, path, rssi):
    return {
        "type": "DISCOVERY",
        "origin": origin,
        "seq": seq,
        "ttl": ttl,
        "path": path,
        "rssi_path": rssi
    }

def make_reverse(origin, seq, path, rssi):
    return {
        "type": "REVERSE",
        "origin": origin,
        "seq": seq,
        "path": path,
        "rssi_path": rssi
    }

def encode(msg):
    return json.dumps(msg).encode()

def decode(raw):
    try:
        return json.loads(raw.decode())
    except:
        return None
