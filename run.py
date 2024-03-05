import os
import shutil
import sys
import threading
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler

class InterruptableHTTPServer(HTTPServer):
    def serve_forever(self):
        try:
            super().serve_forever()
        except KeyboardInterrupt:
            self.server_close()
            print("\nServer stopped.")

def run_dev_server(port=8000):
    print("Starting development server at http://localhost:{}...".format(port))
    original_dir = os.getcwd()
    if not os.path.exists("output"):
        os.mkdir("output")  # Create the output directory if it doesn't exist
        with open("output/index.html", "w") as index_file:
            index_file.write(
                "<!DOCTYPE html>\n<html>\n<head>\n<title>Index</title>\n</head>\n<body>\n<h1>Hello World!</h1>\n</body>\n</html>")

    os.chdir("output")
    server_address = ('', port)
    httpd = InterruptableHTTPServer(server_address, SimpleHTTPRequestHandler)

    # Open browser window
    webbrowser.open_new_tab("http://localhost:{}".format(port))

    # Start the server in a separate thread
    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    while True:
        key = input("Press 'q' to quit, 'r' to reload: ")
        if key.lower() == 'q':
            break
        elif key.lower() == 'r':
            # Reload the page
            webbrowser.reload()
        else:
            print("Invalid input. Press 'q' to quit, 'r' to reload.")

    httpd.server_close()
    print("\nServer stopped.")
    os.chdir(original_dir)

def build():
    pass

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "dev":
        run_dev_server()
        shutil.rmtree("output")
    else:
        print("Usage: python run.py dev")
