import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from backend.pipeline import analyze_text


FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"
MIME_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".json": "application/json; charset=utf-8",
}


class AppHandler(BaseHTTPRequestHandler):
    def _send_json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _serve_static(self, request_path: str) -> None:
        normalized = "index.html" if request_path == "/" else request_path.lstrip("/")
        file_path = (FRONTEND_DIR / normalized).resolve()

        if FRONTEND_DIR not in file_path.parents and file_path != FRONTEND_DIR / "index.html":
            self._send_json(HTTPStatus.FORBIDDEN, {"error": "Forbidden"})
            return

        if not file_path.exists() or not file_path.is_file():
            self._send_json(HTTPStatus.NOT_FOUND, {"error": "Not found"})
            return

        content = file_path.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", MIME_TYPES.get(file_path.suffix.lower(), "application/octet-stream"))
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def do_GET(self) -> None:
        if self.path == "/api/health":
            self._send_json(HTTPStatus.OK, {"status": "ok"})
            return

        self._serve_static(self.path)

    def do_POST(self) -> None:
        if self.path != "/api/analyze":
            self._send_json(HTTPStatus.METHOD_NOT_ALLOWED, {"error": "Method not allowed"})
            return

        content_length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(content_length)

        try:
            payload = json.loads(raw_body.decode("utf-8")) if raw_body else {}
        except json.JSONDecodeError:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "Invalid JSON payload."})
            return

        text = payload.get("text", "")
        if not isinstance(text, str) or not text.strip():
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "Please provide text to analyze."})
            return

        self._send_json(HTTPStatus.OK, analyze_text(text))

    def log_message(self, _format: str, *_args) -> None:
        return


def start_server(host: str = "127.0.0.1", port: int = 3000) -> None:
    server = ThreadingHTTPServer((host, port), AppHandler)
    print(f"Compiler Spell Studio running at http://{host}:{port}")
    server.serve_forever()
