import re

class Router:
    def __init__(self):
        self.routes = {}
        self.dynamic_routes = []

    def render(self, route, content):
        if '<' in route and '>' in route:
            # It's a dynamic route
            self.dynamic_routes.append((re.compile(route), str(content)))
        else:
            self.routes[route] = str(content)

    def run(self, entry):
        route_cases = ""
        for path, content in self.routes.items():
            route_cases += f'"{path}": "{content}",'

        dynamic_routes_js = ""
        for pattern, content in self.dynamic_routes:
            dynamic_routes_js += f"""
                if (new RegExp({pattern.pattern}).test(path)) {{
                    html = `{content}`.replace(new RegExp({pattern.pattern}), path);
                }}
            """

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
    let html = routes[path] || routes[404];

    if (!html) {{
        {dynamic_routes_js}
    }}

    document.getElementById("{entry}").innerHTML = html;
}};

window.onpopstate = handleLocation;
window.route = route;

handleLocation();
"""
        with open('./output/router.js', 'w') as file:
            file.write(js_code)
