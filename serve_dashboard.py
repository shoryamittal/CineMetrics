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
        except (ConnectionResetError, BrokenPipeError):
            pass

    def end_headers(self):
        # Disable aggressive caching for live development/demo
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

    def log_message(self, format, *args):
        # Clean logging
        sys.stderr.write(f"[CPIP {self.log_date_time_string()}] {format % args}\n")

class RobustServer(ThreadingHTTPServer):
    allow_reuse_address = True
    daemon_threads = True

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else PORT
    print(f"[CPIP] Initializing robust dashboard server on port {port}...")
    print(f"[CPIP] Serving directory: {DASHBOARD_DIR}")
    server = RobustServer(('0.0.0.0', port), DashboardHandler)
    print(f"[CPIP] Flagship server active at http://localhost:{port}/")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[CPIP] Server gracefully stopped.")
