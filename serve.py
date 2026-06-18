#!/usr/bin/env python3
"""
TzQuant BP static file server.
Binds to 0.0.0.0 so the page is reachable from the local network.
"""

import socket
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path


HOST = "0.0.0.0"
PORT = 8080


def get_ip_addresses():
    """Return a list of non-loopback IPv4 addresses."""
    ips = []
    try:
        hostname = socket.gethostname()
        infos = socket.getaddrinfo(hostname, None, socket.AF_INET)
        seen = set()
        for info in infos:
            ip = info[4][0]
            if not ip.startswith("127.") and ip not in seen:
                seen.add(ip)
                ips.append(ip)
    except Exception:
        pass
    return ips


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(Path(__file__).parent), **kwargs)

    def log_message(self, format, *args):
        # Quieter logs
        pass


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else PORT
    server = HTTPServer((HOST, port), Handler)

    print(f"TzQuant BP server running on port {port}")
    print(f"Local:   http://127.0.0.1:{port}")

    ips = get_ip_addresses()
    if ips:
        for ip in ips:
            print(f"Network: http://{ip}:{port}")
    else:
        print("Network: could not detect local IP")

    print("Press Ctrl+C to stop")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        server.shutdown()


if __name__ == "__main__":
    main()
