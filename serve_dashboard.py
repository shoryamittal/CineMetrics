#!/usr/bin/env python3
"""
CinePulse / CPIP Enterprise Web Dashboard Server
High-availability threaded server supporting health endpoints and seamless route rewrites.
"""
import os
import sys
import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

PORT = 8080
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DASHBOARD_DIR = os.path.join(BASE_DIR, 'dashboard')

class DashboardHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DASHBOARD_DIR, **kwargs)

    def do_GET(self):
        # Health check endpoints for platform monitors
        if self.path in ('/health', '/api/health', '/status', '/api/status'):
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            payload = json.dumps({
                "status": "UP",
                "service": "CinePulse Decision Intelligence Platform",
                "healthy": True,
                "version": "2.4.0"
            }).encode('utf-8')
            self.wfile.write(payload)
            return

        # Gracefully rewrite /dashboard routes
        if self.path in ('/dashboard', '/dashboard/'):
            self.path = '/'
        elif self.path.startswith('/dashboard/'):
            self.path = self.path[len('/dashboard'):]

        try:
            return super().do_GET()
        except (ConnectionResetError, BrokenPipeError, ConnectionAbortedError, OSError):
            pass

    def end_headers(self):
        # Disable aggressive caching for live development/demo
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

    def log_message(self, format, *args):
        # Clean logging to stdout (prevents PowerShell NativeCommandError on Windows)
        sys.stdout.write(f"[CPIP {self.log_date_time_string()}] {format % args}\n")
        sys.stdout.flush()

import socket

def is_port_available(port: int) -> bool:
    """Checks whether a port is truly available without socket sharing."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('0.0.0.0', port))
            return True
    except OSError:
        return False

class RobustServer(ThreadingHTTPServer):
    allow_reuse_address = (sys.platform != 'win32')
    daemon_threads = True

    def handle_error(self, request, client_address):
        # Gracefully swallow client socket drops without terminating server
        pass

if __name__ == '__main__':
    requested_port = int(sys.argv[1]) if len(sys.argv) > 1 else PORT
    print(f"[CPIP] Initializing robust dashboard server. Target port: {requested_port}...")
    print(f"[CPIP] Serving directory: {DASHBOARD_DIR}")

    server = None
    active_port = requested_port
    candidate_ports = [requested_port] + [p for p in [8081, 8082, 8088, 8888] if p != requested_port]
    for p in candidate_ports:
        if is_port_available(p):
            try:
                server = RobustServer(('0.0.0.0', p), DashboardHandler)
                active_port = p
                break
            except OSError:
                continue

    if server is None:
        sys.exit(f"[CPIP] Error: Could not bind to any candidate port starting from {requested_port}")

    print(f"[CPIP] Flagship server active at http://localhost:{active_port}/")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[CPIP] Server gracefully stopped.")
