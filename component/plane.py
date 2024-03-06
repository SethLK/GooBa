


class Document:
    def __init__(self):
        self.elements = None
        self.head = ""
        self.body_ = ""

    def title(self, text):
        self.head += f"<title>{text}</title>\n"

    def meta(self, **attributes):
        meta_tag = "<meta "
        for key, value in attributes.items():
            meta_tag += f'{key}="{value}" '
        meta_tag += "/>\n"
        self.head += meta_tag

    def body(self, *elements):
        modified_elements = '\n'.join([str(element) for element in elements])
        self.body_ = f"{modified_elements}"

    def build(self):
        html_content = f"""
    <html>
    <head>
    {self.head}
    </head>
    <body>
    {self.body_}
    </body>
    </html>"""

        # Write modified content back to file
        with open('./output/index.html', 'a') as file:
            file.write(html_content)
            print(html_content)
