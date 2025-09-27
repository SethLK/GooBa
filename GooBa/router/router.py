# import re
# from GooBa import Parent
#
# class Router:
#     def __init__(self):
#         self.routes = {}
#         self.dynamic_routes = []
#
#     def render(self, route, content):
#         if isinstance(content, Parent):
#             content = str(content)  # Convert Parent to HTML string
#         if '<' in route and '>' in route:
#             # It's a dynamic route
#             self.dynamic_routes.append((re.compile(route), content))
#         else:
#             # Escape quotes and newlines in content
#             escaped_content = content.replace('"', '\\"').replace('\n', '\\n')
#             self.routes[route] = f'"{escaped_content}"'
#
#     def run(self, entry):
#         # Prepare static routes
#         route_cases = ", ".join(f'"{path}": {content}' for path, content in self.routes.items())
#
#         # Prepare dynamic route handling
#         dynamic_routes_js = ""
#         for pattern, content in self.dynamic_routes:
#             escaped_content = content.replace('"', '\\"').replace('\n', '\\n')
#             dynamic_routes_js += f"""
#                 if (new RegExp({pattern.pattern}).test(path)) {{
#                     html = `{escaped_content}`.replace(new RegExp({pattern.pattern}), path);
#                 }}
#             """
#
#         # Generate JavaScript code
#         js_code = f"""
# const route = (event) => {{
#     event = event || window.event;
#     event.preventDefault();
#     window.history.pushState({{}}, "", event.target.href);
#     handleLocation();
# }};
#
# const routes = {{
#     {route_cases}
# }};
#
# const handleLocation = () => {{
#     const path = window.location.pathname;
#     let html = routes[path];
#
#     if (!html) {{
#         {dynamic_routes_js}
#         if (!html) {{
#             html = "<h2>404 Page Not Found</h2>";
#         }}
#     }}
#
#     document.getElementById("{entry}").innerHTML = html;
# }};
#
# window.onpopstate = handleLocation;
# window.route = route;
#
# handleLocation();
# """
#         with open('./output/router.js', 'w') as file:
#             file.write(js_code)

import re
from .router_js import page  # Assuming this contains the page.js library content

from GooBa import Parent


class Router(object):
    def __init__(self):
        self.routes = {}  # For static routes
        self.dynamic_routes = []  # For dynamic routes

    def render(self, route, param_content):
        content = str(param_content)

        # Check if it's a dynamic route (contains < and >)
        if '<' in route and '>' in route:
            # Convert Flask-style routes to regex patterns
            # Example: "/user/<int:id>/" -> "/user/(\d+)/"
            pattern = route
            # Replace <int:id> with (\d+)
            pattern = re.sub(r'<int:[^>]+>', r'(\\d+)', pattern)
            # Replace <str:slug> or <slug> with ([^/]+)
            pattern = re.sub(r'<str:[^>]+>', r'([^/]+)', pattern)
            pattern = re.sub(r'<[^>]+>', r'([^/]+)', pattern)

            # Escape forward slashes for JavaScript regex
            js_pattern = pattern.replace('/', '\\/')
            self.dynamic_routes.append((js_pattern, content))
        else:
            # Static route - escape quotes and newlines
            # escaped_content = content.replace('"', '\\"').replace('\n', '\\n')
            # self.routes[route] = escaped_content
            self.routes[route] = content

    def run(self, entry):
        """Generate and write the router.js file"""

        # Generate static route registrations
        static_routes_js = []
        for path, content in self.routes.items():
            static_routes_js.append(f'''
page('{path}', () => {{
    render(`{content}`);
}});''')

        static_routes_code = '\n'.join(static_routes_js)

        # Generate dynamic route registrations
        dynamic_routes_js = []
        for pattern, content in self.dynamic_routes:
            # For dynamic routes, we need to capture parameters
            # Simple approach: just render the content as-is
            # You might want to enhance this to handle route parameters
            dynamic_routes_js.append(f'''
page('/{pattern}', (ctx) => {{
    render(`{content}`);
}});''')

        dynamic_routes_code = '\n'.join(dynamic_routes_js)

        # Complete JavaScript code
        js_code = f'''//import page from './page.js';

const render = (html) => {{
    document.getElementById('{entry}').innerHTML = html;
}};

// Static routes
{static_routes_code}

// Dynamic routes  
{dynamic_routes_code}

// 404 handler
page('*', () => {{
    render('<h2>404 Page Not Found</h2>');
}});

page.start();
'''

        # Write the router.js file
        with open('./output/router.js', 'w') as file:
            file.write(js_code)

        # Write the page.js library file
        with open('./output/page.js', 'w') as file:  # Fixed: added missing comma
            file.write(page)