import http.server
import socketserver
import os

PORT = 8000
DIRECTORY = "output"


class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        # Check if the requested file exists in the directory
        requested_path = self.directory + self.path
        if not os.path.exists(requested_path) or os.path.isdir(requested_path):
            self.path = "/index.html"
        return super().do_GET()


# Start the server
with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()
