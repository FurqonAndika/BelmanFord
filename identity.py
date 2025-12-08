'''
Docstring for identity
import subprocess
import os

def get_ip_address():
    try:
        output = subprocess.check_output("hostname -I", shell=True).decode().strip()
        return output.split()[0]
    except:
        return None


def get_mac_address(interface="wlan0"):
    path = f"/sys/class/net/{interface}/address"
    if os.path.exists(path):
        with open(path, "r") as f:
            return f.read().strip()
    return None


def get_node_id(ip):
    try:
        return int(ip.split(".")[-1])
    except:
        return None
'''

import socket
import uuid

def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Connect ke DNS google, tidak benar-benar mengirim paket
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return None

def get_mac_address():
    try:
        mac_num = uuid.getnode()
        mac = ':'.join(['{:02x}'.format((mac_num >> ele) & 0xff)
                       for ele in range(40, -1, -8)])
        return mac
    except:
        return None

def get_node_id(ip):
    if ip is None:
        return None

    # contoh IP: 192.168.50.12
    try:
        last = ip.split(".")[-1]
        return int(last)
    except:
        return None
