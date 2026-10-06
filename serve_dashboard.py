#!/usr/bin/env python3
"""
CinePulse / CPIP Enterprise Web Dashboard Server
Serves the high-fidelity glassmorphic Decision Intelligence web interface.
"""
import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT = 8080
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DASHBOARD_DIR = os.path.join(BASE_DIR, 'dashboard')

class DashboardHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DASHBOARD_DIR, **kwargs)

    def do_GET(self):
        # Gracefully rewrite /dashboard routes
        if self.path in ('/dashboard', '/dashboard/'):
            self.path = '/'
        elif self.path.startswith('/dashboard/'):
            self.path = self.path[len('/dashboard'):]
        return super().do_GET()

    def end_headers(self):
        # Disable aggressive caching for live development/demo
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else PORT
    print(f"[CPIP] Launching Enterprise Decision Dashboard on port {port}...")
    print(f"[CPIP] Serving directory: {DASHBOARD_DIR}")
    server = HTTPServer(('0.0.0.0', port), DashboardHandler)
    print(f"[CPIP] Server active! Access at http://localhost:{port}/")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[CPIP] Server stopped gracefully.")
