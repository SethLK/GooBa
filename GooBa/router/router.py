import re
from .router_js import page

from GooBa import Parent, CreateElement


class Router(object):
    def __init__(self):
        self.routes = {}  # For static routes
        self.dynamic_routes = []  # For dynamic routes
        self.param = None
        self.param_routes = {}

    # def render(self, route, param_content):
    #     #     content = str(param_content)
    #     #
    #     #     if '<' in route and '>' in route:
    #     #         param_names = re.findall(r'<(?:int:|str:)?([^>]+)>', route)
    #     #         js_route = route
    #     #         js_route = re.sub(r'<([^>]+)>', r':\1', js_route)
    #     #         self.dynamic_routes.append((js_route, content, param_names))
    #     #     else:
    #     #         self.routes[route] = content

    def render(self, route, param_content):
        if isinstance(param_content, CreateElement):
            # Generate DOM code instead of string HTML
            content, root_var = param_content.to_js_dom()
            content = "\n".join(content) + f"\ndocument.getElementById('root').appendChild({root_var});"
        else:
            content = str(param_content)

        if '<' in route and '>' in route:
            param_names = re.findall(r'<(?:int:|str:)?([^>]+)>', route)
            js_route = re.sub(r'<([^>]+)>', r':\1', route)
            self.dynamic_routes.append((js_route, content, param_names))
        else:
            self.routes[route] = content

    def _convert_to_regex(self, path: str) -> str:
        """Convert route like '/<id>/<name>' to regex pattern"""
        # Replace <param> with named capture groups
        pattern = re.sub(r'<(\w+)>', r'(?P<\1>[^/]+)', path)
        return f'^{pattern}$'

    # def _escape_for_js(self, content):
    #     """Escape HTML content for JavaScript template literals"""
    #     # Escape backslashes first
    #     content = content.replace('\\', '\\\\')
    #     # Escape backticks
    #     content = content.replace('`', '\\`')
    #     # Escape $ for template literals
    #     content = content.replace('$', '\\$')
    #     # Escape newlines
    #     content = content.replace('\n', '\\n')
    #     # Escape carriage returns
    #     content = content.replace('\r', '\\r')
    #     # Escape tabs
    #     content = content.replace('\t', '\\t')
    #     return content

    # def _escape_for_js(self, content):
    #     if "document.createElement" in content:
    #         return content  # it's JS DOM code, not HTML

    def _escape_for_js(self, content):
        if "document.createElement" in content:
            return content  # it's JS DOM code, not HTML
        return (
            content.replace("\\", "\\\\")
            .replace("`", "\\`")
            .replace("$", "\\$")
            .replace("\n", "\\n")
            .replace("\r", "\\r")
            .replace("\t", "\\t")
        )

    def _get_param_replacement_code(self, param_names):
        """Generate JavaScript code for parameter replacement"""
        replacements = []
        for param_name in param_names:
            # Handle multiple occurrences of the same parameter in the content
            # Use regex with global flag to replace all occurrences
            replacements.append(f'html = html.replace(new RegExp(`{{{{{param_name}}}}}`, "g"), ctx.params.{param_name} || "");')
        return '\n    '.join(replacements)

    def run(self, entry):
        """Generate and write the router.js file"""

        # Generate static route registrations
#         static_routes_js = []
#         for path, content in self.routes.items():
#             # Escape content for JavaScript
#             escaped_content = self._escape_for_js(content)
#             static_routes_js.append(f'''
# page('{path}', () => {{
#     render(`{escaped_content}`);
# }});''')
#
#         static_routes_code = '\n'.join(static_routes_js)

        # Generate static route registrations
        static_routes_js = []
        for path, content in self.routes.items():
            if "document.createElement" in content:
                # It's DOM-based JS
                static_routes_js.append(f'''
        page('{path}', () => {{
        {content}
        }});''')
            else:
                # HTML string fallback
                escaped_content = self._escape_for_js(content)
                static_routes_js.append(f'''
        page('{path}', () => {{
            render(`{escaped_content}`);
        }});''')

        static_routes_code = '\n'.join(static_routes_js)
        # Generate dynamic route registrations
#         dynamic_routes_js = []
#         for js_route, content, param_names in self.dynamic_routes:
#             # Escape content for JavaScript
#             escaped_content = self._escape_for_js(content)
#
#             if param_names:
#                 # Generate parameter replacement logic
#                 param_replacements = self._get_param_replacement_code(param_names)
#
#                 dynamic_routes_js.append(f'''
# page('{js_route}', (ctx) => {{
#     let html = `{escaped_content}`;
#     {param_replacements}
#     render(html);
# }});''')
#             else:
#                 dynamic_routes_js.append(f'''
# page('{js_route}', (ctx) => {{
#     render(`{escaped_content}`);
# }});''')

        # Generate dynamic route registrations
        dynamic_routes_js = []
        for js_route, content, param_names in self.dynamic_routes:
            if "document.createElement" in content:
                # Replace placeholders {{param}} in DOM creation JS
                for param in param_names:
                    content = content.replace(f"{{{{{param}}}}}", f"${{ctx.params.{param}}}")
                dynamic_routes_js.append(f'''
                    page('{js_route}', (ctx) => {{
                        {content}
                    }});''')

            else:
                escaped_content = self._escape_for_js(content)
                if param_names:
                    param_replacements = self._get_param_replacement_code(param_names)
                    dynamic_routes_js.append(f'''
        page('{js_route}', (ctx) => {{
            let html = `{escaped_content}`;
            {param_replacements}
            render(html);
        }});''')
                else:
                    dynamic_routes_js.append(f'''
        page('{js_route}', (ctx) => {{
            render(`{escaped_content}`);
        }});''')

        dynamic_routes_code = '\n'.join(dynamic_routes_js)

        # Complete JavaScript code
        js_code = f'''// Router generated by Packed Framework

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
        with open('./output/main.js', 'w') as file:
            file.write(js_code)

        # Write the page.js library file
        with open('./output/page.js', 'w') as file:
            file.write(page)
