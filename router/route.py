class Route:

    def __init__(self):
        self.routes = {
            "/": "<h1>Home Page</h1>",
            "/about": "<h1>About Page</h1>",
            "/contact": "<h1>Contact Page</h1>"
        }

    def add_route(self, path, content):
        self.routes[path] = content

    def update_route(self, path, content):
        if path in self.routes:
            self.routes[path] = content
        else:
            print(f"Route '{path}' not found.")

    def run(self):
