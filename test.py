routes = {
    "/": "<h1>Home Page</h1>",
    "/about": "<h1>About Page</h1>",
    "/contact": "<h1>Contact Page</h1>"
}


routes["/404"] = "404"

Route = ""

for path, content in routes.items():
    Route += f"""
        case '{path}':
            renderContent("{content}");  
            break;
"""


Tester = f"""function handleRoute() {{
    const path = window.location.pathname;
    switch (path) {{
        {Route}
        default:
            renderContent("<h1>404 Page</h1>");   
            break;
    }}
}}
"""

print(Tester)
