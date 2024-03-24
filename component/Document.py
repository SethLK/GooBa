from hmr.hmr import javascript


class Document:
    def __init__(self):
        self.head = ""
        self.body_ = ""
        self.styles = []

    def title(self, text):
        self.head += f"<title>{text}</title>\n"

    def meta(self, **attributes):
        meta_tag = "<meta "
        for key, value in attributes.items():
            meta_tag += f'{key}="{value}" '
        meta_tag += "/>\n"
        self.head += meta_tag

    def add_style(self, *style):
        self.styles.extend(style)

    def body(self, *elements: object) -> object:
        modified_elements = '\n'.join([str(element) for element in elements])
        self.body_ = f"{modified_elements}"

    def build(self):
        # Constructing the HTML content
        styles_str = '\n'.join(map(str, self.styles))  # Concatenate all styles into a single string
        html_content = f"""<!DOCTYPE html>
        <html>
        <head>
        <style>
        {styles_str}
        </style>
        {self.head}
        </head>
        <body>
        {self.body_}
        </body>
        
        <script src="./hmr.js"></script>
        <script src="./script.js"></script>
        </html>
        """

        # Write modified content back to file
        with open('./output/index.html', 'w') as file:
            file.write(html_content)
            print(html_content)



        with open('./output/hmr.js', 'w') as file:
            file.write(javascript)