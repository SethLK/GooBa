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
    routes = {
        "/": "<h1>Home Page</h1>",
        "/about": "<h1>About Page</h1>",
        "/contact": "<h1>Contact Page</h1>"
    }
    def page(self, path, content):
