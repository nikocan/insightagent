"""Minimal HTTP server exposing the InsightAgent API without external deps."""

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

from fastapi.application import TestClient

from .main import app

client = TestClient(app)


class InsightAgentHandler(BaseHTTPRequestHandler):
    """Serve GET requests by delegating to the FastAPI shim test client."""

    def do_GET(self) -> None:  # noqa: N802 - required name by BaseHTTPRequestHandler
        parsed_path = urlparse(self.path)
        response = client.get(parsed_path.path)
        payload = response.json()
        body = json.dumps(payload, default=str).encode()
        self.send_response(response.status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args) -> None:  # noqa: A003 - align with base signature
        """Silence default logging to keep console clean."""

        return


def run(port: int = 8000) -> None:
    """Start the development HTTP server."""

    server_address = ("", port)
    httpd = HTTPServer(server_address, InsightAgentHandler)
    print(f"InsightAgent server running at http://localhost:{port}")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
