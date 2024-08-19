class CreateElement:
    def __init__(self, tag, **attributes):
        self.tag = tag
        self.attributes = attributes
        self.text = None
        self.children = []
        self.style = {}  # Use a dictionary for inline styles

    def appendChild(self, *children):
        self.children.extend(children)

    def _format_style(self):
        if not self.style:
            return ''
        style_items = []
        for key, value in self.style.items():
            style_items.append(f'{key}: {value};')
        return ' '.join(style_items)

    def __str__(self):
        attribute_string = ' '.join([f'{key}="{value}"' for key, value in self.attributes.items()])

        # Add inline style if it exists
        style_string = self._format_style()
        if style_string:
            attribute_string += f' style="{style_string}"'

        if 'className' in self.attributes:
            attribute_string = attribute_string.replace('className', 'class')

        if self.text is not None:
            content = f'{self.text}'
        else:
            content = ''.join(str(child) for child in self.children)

        if self.text:
            return f'<{self.tag} {attribute_string}>{content}</{self.tag}>\n'
        else:
            children_ = ''.join(str(child) for child in self.children)
            return f'<{self.tag} {attribute_string}>\n{children_}\n</{self.tag}>'

    def __add__(self, other):
        if isinstance(other, CreateElement):
            return self.__str__() + other.__str__()
        else:
            return self.__str__() + str(other)

class Image(CreateElement):
    def __init__(self, tag, **attributes):
        super().__init__('img', **attributes)
        self.src = None
        self.alt = None
        self.height = None
        self.width = None
        self.attributes = attributes

    def __str__(self):
        attribute_string = ' '.join([f'{key}="{value}"' for key, value in self.attributes.items()])
        alt_attribute = f'alt="{self.alt}"' if self.alt else ''
        return f'<img src="{self.src}" {alt_attribute} {attribute_string}>'

    def __add__(self, other):
        if isinstance(other, Image):
            return self.__str__() + other.__str__()
        else:
            return self.__str__() + str(other)

class Link(CreateElement):
    def __init__(self, tag, **attributes):
        super().__init__('img', **attributes)
        self.href = None
        self.attributes = attributes