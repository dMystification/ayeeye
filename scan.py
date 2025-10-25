import socket
import json
from datetime import datetime
from pathlib import Path

def scan_host(host, ports):
    print(f"Scanning {host}...\n")
    results = []

    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((host, port))
            status = "open" if result == 0 else "closed"
            results.append({"port": port, "status": status})
            if status == "open":
                print(f"[+] Port {port} is OPEN")
            sock.close()
        except Exception as e:
            results.append({"port": port, "status": f"error: {e}"})
            print(f"Error scanning port {port}: {e}")

    print("\nScan complete.")
    return results


def save_reports(host, results):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_dir = Path("reports")
    report_dir.mkdir(exist_ok=True)

    # Save JSON report
    json_path = report_dir / f"{host}_scan_{timestamp}.json"
    with open(json_path, "w") as f:
        json.dump(results, f, indent=4)

    # Generate simple HTML report
    html_path = report_dir / f"{host}_scan_{timestamp}.html"
    html_content = f"""
    <html>
    <head>
        <title>Scan Report for {host}</title>
        <style>
            body {{ font-family: Arial, sans-serif; background-color: #0d1117; color: #e6edf3; }}
            table {{ border-collapse: collapse; width: 50%; margin: 20px auto; }}
            th, td {{ border: 1px solid #30363d; padding: 8px 12px; text-align: left; }}
            th {{ background-color: #161b22; }}
            tr:nth-child(even) {{ background-color: #161b22; }}
            h2 {{ text-align: center; }}
        </style>
    </head>
    <body>
        <h2>Scan Report for {host}</h2>
        <table>
            <tr><th>Port</th><th>Status</th></tr>
            {''.join(f"<tr><td>{r['port']}</td><td>{r['status']}</td></tr>" for r in results)}
        </table>
        <p style='text-align:center;'>Generated at {timestamp}</p>
    </body>
    </html>
    """

    with open(html_path, "w") as f:
        f.write(html_content)

    print(f"\n[+] Reports saved to:")
    print(f"   JSON: {json_path}")
    print(f"   HTML: {html_path}")


if __name__ == "__main__":
    target = input("Enter target IP or hostname: ")
    ports = [21, 22, 80, 135, 443, 445, 3389]
    results = scan_host(target, ports)
    save_reports(target, results)
