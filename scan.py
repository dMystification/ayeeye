import socket

def scan_host(host, ports):
    print(f"Scanning {host}...\n")
    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((host, port))
            if result == 0:
                print(f"[+] Port {port} is OPEN")
            sock.close()
        except Exception as e:
            print(f"Error scanning port {port}: {e}")
    print("\nScan complete.")

if __name__ == "__main__":
    target = input("Enter target IP or hostname: ")
    ports = [21, 22, 80, 135, 443, 445, 3389]
    scan_host(target, ports)
