class Element:
    def __init__(self, tag, **attributes):
        self.tag = tag
        self.attributes = attributes
        self.text = None
        self.children = []

    def appendChild(self, *children):
        self.children.extend(children)

    def __str__(self):
        attribute_string = ' '.join([f'{key}="{value}"' for key, value in self.attributes.items()])

        if 'className' in self.attributes:
            attribute_string = attribute_string.replace('className', 'class')

        if self.text is not None:
            return f'<{self.tag} {attribute_string}>{self.text}</{self.tag}>\n'
        else:
            children_ = ''.join(str(child) for child in self.children)
            return f'<{self.tag} {attribute_string}>\n{children_}\n</{self.tag}>'


    def __add__(self, other):
        if isinstance(other, Element):
            return self.__str__() + other.__str__()
        else:
            return self.__str__() + str(other)


class Link(Element):
    def __init__(self, href, **attributes):
        super().__init__('a', **attributes)
        self.attributes['href'] = href
