import os
import sys

def create_project_structure(project_name):
    # Define the directory structure
    project_dir = project_name
    files = {
        'main.py': '''from GooBa import Document, Element

# Initialize Document and Router
doc = Document()

h1 = Element("h1")
h1.text = "Hello World"

doc.body(h1)
doc.build()

''',
        'run.py': '''import http.server
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

'''
    }

    # Create the project directory
    os.makedirs(project_dir, exist_ok=True)

    # Create the files with the specified content
    for filename, content in files.items():
        with open(os.path.join(project_dir, filename), 'w') as file:
            file.write(content)

    print(f"Project '{project_name}' created successfully.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: gooba-new <project_name>")
        sys.exit(1)

    project_name = sys.argv[1]
    create_project_structure(project_name)
