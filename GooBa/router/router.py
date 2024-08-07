import re
from GooBa import Parent

class Router:
    def __init__(self):
        self.routes = {}
        self.dynamic_routes = []

    def render(self, route, content):
        if isinstance(content, Parent):
            content = str(content)  # Convert Parent to HTML string
        if '<' in route and '>' in route:
            # It's a dynamic route
            self.dynamic_routes.append((re.compile(route), content))
        else:
            # Escape quotes and newlines in content
            escaped_content = content.replace('"', '\\"').replace('\n', '\\n')
            self.routes[route] = f'"{escaped_content}"'

    def run(self, entry):
        # Prepare static routes
        route_cases = ", ".join(f'"{path}": {content}' for path, content in self.routes.items())

        # Prepare dynamic route handling
        dynamic_routes_js = ""
        for pattern, content in self.dynamic_routes:
            escaped_content = content.replace('"', '\\"').replace('\n', '\\n')
            dynamic_routes_js += f"""
                if (new RegExp({pattern.pattern}).test(path)) {{
                    html = `{escaped_content}`.replace(new RegExp({pattern.pattern}), path);
                }}
            """

        # Generate JavaScript code
        js_code = f"""
const route = (event) => {{
    event = event || window.event;
    event.preventDefault();
    window.history.pushState({{}}, "", event.target.href);
    handleLocation();
}};

const routes = {{
    {route_cases}
}};

const handleLocation = () => {{
    const path = window.location.pathname;
    let html = routes[path];

    if (!html) {{
        {dynamic_routes_js}
        if (!html) {{
            html = "<h2>404 Page Not Found</h2>";
        }}
    }}

    document.getElementById("{entry}").innerHTML = html;
}};

window.onpopstate = handleLocation;
window.route = route;

handleLocation();
"""
        with open('./output/router.js', 'w') as file:
            file.write(js_code)
