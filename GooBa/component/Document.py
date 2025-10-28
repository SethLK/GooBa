import os

from GooBa.hmr.hmr import javascript


class Document:
    def __init__(self):
        self.head = ""
        self.body_ = ""
        self.styles = []
        self.extern_js = []

    def title(self, text):
        self.head += f"<title>{text}</title>\n"

    def meta(self, **attributes):
        meta_tag = "<meta "
        for key, value in attributes.items():
            meta_tag += f'{key}="{value}" '
        meta_tag += "/>\n"
        self.head += meta_tag

    def body(self, *elements: object) -> object:
        modified_elements = '\n'.join([str(element) for element in elements])
        self.body_ = f"{modified_elements}"

    def appendHead(self, newHead):
        self.head += str(newHead) + "\n"

    def add_EternalJs(self, extern_JS):
        if extern_JS:
            self.extern_js.append(extern_JS)

    def build(self):
        styles_str = '\n'.join(map(str, self.styles))
        external_js_str = '\n'.join(f'<script src="{path}.js"></script>' for path in self.extern_js)

        html_content = f"""<!DOCTYPE html>
        <html>
        <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <style>
        {styles_str}
        </style>
        {self.head}
        </head>
        <body>
        {self.body_}
        </body>
        
        <div id="root">
        
        </div>
        <script src="/page.js"></script>
        <script src="/main.js"></script>
        {external_js_str}
        <script src="/hmr.js"></script>
        
        </html>
        """
        if not os.path.exists('./output'):
            os.makedirs('./output')

        with open('./output/index.html', 'w') as file:
            file.write(html_content)
            # print(html_content)

        with open('./output/hmr.js', 'w') as file:
            file.write(javascript)
