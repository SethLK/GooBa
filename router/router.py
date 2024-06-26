class Router:
    def __init__(self):
        self.routes = {}

    def render(self, route, content):
        self.routes[route] = content

    def run(self, entry):
        route_cases = ""
        for path, content in self.routes.items():
            route_cases += f"""
                case '{path}':
                    renderContent(`{content}`); 
                    break;
            """

        js_code = f"""
function handleRoute() {{
    const path = window.location.pathname;
    switch (path) {{
        {route_cases}
        default:
            renderContent("<h1>404 Page</h1>");   
            break;
    }}
}}

function renderContent(content) {{
    const {entry} = document.getElementById("{entry}");
    if ({entry}) {{
        {entry}.innerHTML = content;
    }}
}}

document.addEventListener('DOMContentLoaded', () => {{
    const links = document.querySelectorAll('nav a');
    links.forEach(link => {{
        link.addEventListener('click', event => {{
            event.preventDefault();
            const href = link.getAttribute('href');
            history.pushState(null, null, href);
            handleRoute(); 
        }});
    }});
}});

window.addEventListener('popstate', handleRoute);

function handleLocation() {{
    handleRoute();
}}

function action(route) {{
    history.pushState(null, null, route);
    handleLocation();
}}

handleLocation();
"""
        with open('./output/script.js', 'w') as file:
            file.write(js_code)