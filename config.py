import netifaces

def get_ip():
    return netifaces.ifaddresses("wlan0")[netifaces.AF_INET][0]["addr"]

def get_node_id():
    # last octet from IP
    ip = get_ip()
    return int(ip.split(".")[-1])
