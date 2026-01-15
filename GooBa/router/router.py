import re
from .router_js import page

from GooBa import Parent, CreateElement

class Router(object):
    def __init__(self):
        self.routes = {}  # For static routes
        self.dynamic_routes = []  # For dynamic routes
        self.param = None
        self.param_routes = {}

    def _escape_for_js(self, content):
        return (
            content.replace("\\", "\\\\")
                        .replace("`", "\\`")
                        .replace("$", "\\$")
                        .replace("\n", "\\n")
                        .replace("\r", "\\r")
                        .replace("\t", "\\t")
        )

    def render(self, route, content):
        if hasattr(content, "to_h"):
            content = content.to_h()
        if ':' in route:
            param = re.findall(r":(\w+)", route)
            self.dynamic_routes.append((route, param, content))

        else:
            self.routes[route] = content

    def run(self, entry):
        static_routes_js = []
        for path, content in self.routes.items():
            if content.startswith("function"):
                static_routes_js.append(f"""
                page('{path}', () => {{
                    render({content});
                }});
                """)
            else:
            # print(content)
                static_routes_js.append(f"""
                page('{path}', () => {{
                    render(() => {content});
                }});
                """)

        static_routes_code = '\n'.join(static_routes_js)
        # print(static_routes_code)

        dynamic_routes_js = []
        for route, param, content in self.dynamic_routes:
            # print(self.dynamic_routes)
            dynamic_routes_js.append(f"""
            page('{route}', (ctx) => {{
                render(() => {content});
            }});
            """)

        dynamic_routes_code = '\n'.join(dynamic_routes_js)
        # print(dynamic_routes_code)
        js_code = (f'''
import {{ createApp, h, Create, withHooks, useRequest, useOnce, hFragment }} from "/dist/gooba.js";
        function render(componentFn) {{
          createApp({{view: componentFn }}).mount(document.getElementById("{entry}"));
        }}


        // Static routes
        {static_routes_code}

        // Dynamic routes
        {dynamic_routes_code}

        // 404 handler
        page('*', () => {{
            render('<h2>404 Page Not Found</h2>');
        }});

        page.start();
        '''.rstrip())

                # Write the router.js file
        with open('./output/main.js', 'w') as file:
            file.write(js_code)

                # Write the page.js library file
        with open('./output/page.js', 'w') as file:
            file.write(page)
