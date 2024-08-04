class Parent:
    def __init__(self, tag, **attributes):
        self.tag = tag
        self.attributes = attributes
        self.children = []

    def appendChild(self, *children):
        self.children.extend(children)

    def __str__(self):
        attribute_string = ' '.join([f'{key}="{value}"' for key, value in self.attributes.items()])
        children_string = '\n'.join(["\t" + str(child) for child in self.children])
        return f'<{self.tag} {attribute_string}>\n{children_string}\n\t</{self.tag}>\n'
