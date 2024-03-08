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