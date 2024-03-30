class Style:
    def __init__(self, selector):
        self.selector = selector
        self.properties = {}

    def add_property(self, property_name, value):
        self.properties[property_name] = value

    def __str__(self):
        # Construct the CSS string for the selector and its properties
        css = f"{self.selector} {{\n"
        for prop, value in self.properties.items():
            css += f"    {prop.replace('_', '-')} : {value};\n"
        css += "}\n"
        return css


# external style

class Css:
    def __init__(self, style, fileName=None):
        self.style = style
        self.fileName = fileName

    def render(self):
        with open(f'./output/{self.fileName}.css', 'w') as file:
            file.write(self.style)

    def apply(self):
        if self.fileName:
            link_tag = f'<link rel="stylesheet" type="text/css" href="{self.fileName}.css">'
            return link_tag
        elif self.style:
            style_tag = f'<style>{self.style}</style>'
            return style_tag
        else:
            return ''

    def __str__(self):
        return self.style

    def remove(self):
        pass
