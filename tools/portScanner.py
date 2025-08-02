import socket
from config.config import ports

def scan_ports(target):
    print(f"Scanning ports http/s service on: {target}")
    if target.__contains__('https://'):
        target = target.replace('https://', '')
    elif target.__contains__('http://'):
        target = target.replace('http://', '')
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        if result == 0:
            print(f"Port {port} is open")
        sock.close()





