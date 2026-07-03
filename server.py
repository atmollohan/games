import json
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse

from games import checkers, chess, tictactoe

PORT = int(os.environ.get("PORT", 8001))
HOST = os.environ.get("HOST", "0.0.0.0")

GAMES = {
    "chess": chess,
    "checkers": checkers,
    "tictactoe": tictactoe,
}


class Handler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        super().end_headers()

    def _send_json(self, data: dict, status: int = 200):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_body(self) -> dict:
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return {}
        raw = self.rfile.read(length)
        return json.loads(raw)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/health":
            self._send_json({"status": "ok"})
            return

        # Game state endpoint: /api/<game>/state
        parts = path.strip("/").split("/")
        if len(parts) == 3 and parts[0] == "api" and parts[2] == "state":
            game_mod = GAMES.get(parts[1])
            if game_mod:
                self._send_json(game_mod.state())
                return

        super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        parts = parsed.path.strip("/").split("/")

        # /api/<game>/init
        if len(parts) == 3 and parts[0] == "api" and parts[2] == "init":
            game_mod = GAMES.get(parts[1])
            if game_mod:
                self._send_json(game_mod.init_game())
                return

        # /api/<game>/move  (chess, checkers)
        # /api/<game>/action (tictactoe)
        if len(parts) == 3 and parts[0] == "api" and parts[2] in ("move", "action"):
            game_mod = GAMES.get(parts[1])
            if game_mod:
                body = self._read_body()
                result = game_mod.handle_action(body)
                status = 200 if "error" not in result else 400
                self._send_json(result, status)
                return

        self._send_json({"error": "Not found"}, 404)

    # Serve index.html for / (from static/ directory)
    def translate_path(self, path):
        root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
        if path == "/" or path == "":
            return os.path.join(root, "index.html")
        return os.path.join(root, path.lstrip("/"))


os.chdir(os.path.dirname(os.path.abspath(__file__)))

with HTTPServer((HOST, PORT), Handler) as httpd:
    print(f"Serving at http://{HOST}:{PORT}")
    httpd.serve_forever()
