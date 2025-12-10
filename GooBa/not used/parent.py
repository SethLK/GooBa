class Parent:
    def __init__(self, tag, **attributes):
        self.tag = tag
        self.attributes = attributes
        self.children = []

    def appendChild(self, *children):
        self.children.extend(children)

    def __str__(self):
        # Build attributes string, handle case where attributes might be empty
        if self.attributes:
            attribute_string = ' '.join(f'{key}="{value}"' for key, value in self.attributes.items())
            attributes_part = f' {attribute_string}'
        else:
            attributes_part = ''

        # Convert children to HTML, taking care of nested elements
        children_string = ''.join(str(child) for child in self.children)

        # Generate HTML string
        return f'<{self.tag}{attributes_part}>{children_string}</{self.tag}>'
