# Client Side Rendering

class Rendering:
    def __init__(self, url: str, selector: str, keys: str):
        self.url: str = url
        self.selector: str = selector
        self.keys: str = keys

    def render(self):
        js_code = f"""
            async function fetchData() {{
                try {{
                    const response = await fetch('{self.url}');
                    if (!response.ok) {{
                        throw new Error('Network response was not ok');
                    }}
                    const data = await response.json();
                    document.querySelector("{self.selector}").innerText = data.{self.keys};
                }} catch (error) {{
                    console.error('Error:', error);
                }}
            }}

            document.addEventListener("DOMContentLoaded", function() {{
                fetchData();
            }});
        """
        with open("./output/CSR.js", 'w') as file:
            file.write(js_code)
