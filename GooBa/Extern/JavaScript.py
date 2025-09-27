class CodeBlock:
    def __init__(self, code: str, filename: str = None):
        self.code = code
        self.filename = filename

    def save_to_file(self):
        if self.filename:
            try:
                with open(f'./output/{self.filename}.js', 'w') as file:
                    file.write(self.code)
            except IOError as e:
                print(f"Error writing to file: {e}")
                return None
            return self.filename
        return None

    def get_code_tag(self, type):
        if self.code:
            if type:
                return f'<script type="{type}">{self.code}</script>'
            else:
                return f'<script>{self.code}</script>'
        return None

    def __str__(self):
        return self.code
