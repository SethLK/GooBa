import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler

def run_dev_server(port=8000):
    print("Starting development server at http://localhost:{}...".format(port))
    os.chdir("output")  # Change to your output directory where your static files are located
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    httpd.serve_forever()

def build():
    pass

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "dev":
        run_dev_server()
    else:
        print("Usage: python run.py dev")
