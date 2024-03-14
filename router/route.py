script = """


function handleRoute() {
    const path = window.location.pathname;
    switch (path) {
        case '/about':
            renderContent("<h1>About Page</h1>");
            break;
        case '/contact':
            renderContent("<h1>Contact Page</h1>");
            break;
        default:
            renderContent("<h1>Home Page</h1>");
            break;
    }
}

function renderContent(content) {
    const root = document.getElementById("root");
    if (root) {
        root.innerHTML = content;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const links = document.querySelectorAll('nav a');
    links.forEach(link => {
        link.addEventListener('click', event => {
            event.preventDefault();
            const href = link.getAttribute('href');
            history.pushState(null, null, href);
            handleRoute(); 
        });
    });
});


window.addEventListener('popstate', handleRoute);

function handleLocation() {
    handleRoute();
}

const routes = {
    "/": "<h1>Home Page</h1>",
    "/about": "<h1>About Page</h1>",
    "/contact": "<h1>Contact Page</h1>"
};

function action(route) {
    history.pushState(null, null, route);
    handleLocation();
}

handleLocation();
"""

class Route:
    def __init__(self, path, content):
        self.path = path
        self.content = content


class Router:
    def __init__(self):
        self.routes = []

    def add_route(self, route):
        self.routes.append(route)

    def handle_route(self, path):
        for route in self.routes:
            if route.path == path:
                return route.content
        return "<h1>404 - Not Found</h1>"


# Usage example
router = Router()
router.add_route(Route("/", "<h1>Home Page</h1>"))
router.add_route(Route("/about", "<h1>About Page</h1>"))
router.add_route(Route("/contact", "<h1>Contact Page</h1>"))

# You can add more routes as needed

# Example of handling a route
path = "/about"
content = router.handle_route(path)
print(content)  # Output: <h1>About Page</h1>
