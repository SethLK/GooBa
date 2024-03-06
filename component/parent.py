class Parent:
    def __init__(self, tag, **attributes):
        self.tag = tag
        self.attributes = attributes
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def __str__(self):
        attribute_string = ' '.join([f'{key}="{value}"' for key, value in self.attributes.items()])
        children_string = '\n'.join([str(child) for child in self.children])
        return f'<{self.tag} {attribute_string}>\n\t{children_string}\n</{self.tag}>\n\t'
