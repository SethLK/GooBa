class Rendering:
    def __init__(self, url: str, selectors: dict):
        self.url = url
        self.selectors = selectors

    def generate_fetch_code(self):
        fetch_code = ""
        for key, selector in self.selectors.items():
            fetch_code += f"""
                document.querySelector("{selector}").innerText = data.{key};\n
            """
        return fetch_code

    def render(self):
        js_code = f"""
            async function fetchData() {{
                try {{
                    const response = await fetch('{self.url}');
                    if (!response.ok) {{
                        throw new Error('Network response was not ok');
                    }}
                    const data = await response.json();
                    {self.generate_fetch_code()}
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
