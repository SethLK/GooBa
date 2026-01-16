


class CreateStyle:
    def __init__(self, fileName=None):
        self.fileName = fileName
        self.styles = {}

    def style(self, selector, properties):
        if selector not in self.styles:
            self.styles[selector] = {}
        self.styles[selector].update(properties)

    def __str__(self):
        css_string = ""
        for selector, properties in self.styles.items():
            css_string += f"\n{selector} {{\n"
            for prop, value in properties.items():
                css_string += f"    {prop.replace('_', '-')} : {value};\n"
            css_string += "}\n"

        if self.fileName:
            with open(f'./output/{self.fileName}.css', 'w') as file:
                file.write(css_string)
            return f'<link rel="stylesheet" type="text/css" href="{self.fileName}.css">'
        else:
            return f'<style>{css_string}</style>'

