import http.server
import pathlib


def create_http_dropper(ip: str, port: int, content: bytes):
    """Return an HTTP Handler that always return the specified content."""

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(http.HTTPStatus.OK)
            self.send_header("Content-Type", 'application/octet-stream')
            self.send_header("Content-Length", len(content))
            self.end_headers()
            self.wfile.write(content)

    return http.server.HTTPServer((ip, port), Handler)


def create_http_exfiltrator(ip: str, port: int, path: pathlib.Path):
    """Return an HTTP Handler that always write the received content to the specified file."""

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_POST(self):

            content_length = int(self.headers.get('Content-Length'))

            with path.open("wb") as writer:
                writer.write(self.rfile.read(content_length))

            self.send_response(http.HTTPStatus.OK)
            self.end_headers()

    return http.server.HTTPServer((ip, port), Handler)
