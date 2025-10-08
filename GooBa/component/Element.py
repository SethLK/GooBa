from enum import Enum


# class CreateElement:
#     def __init__(self, tag, **attributes):
#         self.tag = tag
#         self.attributes = attributes
#         self.text = None
#         self.children = []
#         self.style = {}  # Use a dictionary for inline styles
#
#     def appendChild(self, *children):
#         self.children.extend(children)
#
#     def _format_style(self):
#         if not self.style:
#             return ''
#         style_items = []
#         for key, value in self.style.items():
#             style_items.append(f'{key}: {value};')
#         return ' '.join(style_items)
#
#     def __str__(self):
#         attribute_string = ' '.join([f'{key}="{value}"' for key, value in self.attributes.items()])
#
#         # Add inline style if it exists
#         style_string = self._format_style()
#         if style_string:
#             attribute_string += f' style="{style_string}"'
#
#         if 'className' in self.attributes:
#             attribute_string = attribute_string.replace('className', 'class')
#
#         if self.text is not None:
#             content = f'{self.text}'
#         else:
#             content = ''.join(str(child) for child in self.children)
#
#         if self.text:
#             return f'<{self.tag} {attribute_string}>{content}</{self.tag}>'
#         else:
#             children_ = ''.join(str(child) for child in self.children)
#             return f'<{self.tag} {attribute_string}>{children_}</{self.tag}>'
#
#     def __add__(self, other):
#         if isinstance(other, CreateElement):
#             return self.__str__() + other.__str__()
#         else:
#             return self.__str__() + str(other)

class CreateElement:
    def __init__(self, tag, attributes=None, *children):
        self.tag = tag
        self.attributes = attributes or {}
        self.children = list(children)
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
        # Format attributes
        attribute_items = []
        for key, value in self.attributes.items():
            if key == 'className':
                key = 'class'
            attribute_items.append(f'{key}="{value}"')

        attribute_string = ' '.join(attribute_items)

        # Add inline style if it exists
        style_string = self._format_style()
        if style_string:
            if attribute_string:
                attribute_string += f' style="{style_string}"'
            else:
                attribute_string = f'style="{style_string}"'

        # Handle children and text content
        if self.children:
            content = ''.join(str(child) for child in self.children)
        else:
            content = ''

        # Build the HTML string
        if attribute_string:
            return f'<{self.tag} {attribute_string}>{content}</{self.tag}>'
        else:
            return f'<{self.tag}>{content}</{self.tag}>'

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


class CreateLink(CreateElement):
    def __init__(self, tag, **attributes):
        super().__init__('a', **attributes)
        self.href = None
        self.attributes = attributes

    def __str__(self):
        attribute_string = ' '.join([f'{key}="{value}"' for key, value in self.attributes.items()])
        return f'<a href="{self.href}" {attribute_string}>'


class Methods(Enum):
    GET = "get"
    POST = "post"
    PUT = "put"
    PATCH = "patch"
    DELETE = "delete"


class CreateForm(CreateElement):
    def __init__(self, action='', method='POST', **attributes):
        super().__init__('form', **attributes)
        self.action = action
        self.method = method

    def add_input(self, input_type, name, value='', **attributes):
        input_attributes = {
            'type': input_type,
            'name': name,
            'value': value,
            **attributes
        }
        input_tag = CreateElement('input', **input_attributes)
        self.appendChild(input_tag, "<br>")

    def add_textarea(self, name, rows=4, cols=50, **attributes):
        textarea_attributes = {
            'name': name,
            'rows': rows,
            'cols': cols,
            **attributes
        }
        textarea_tag = CreateElement('textarea', **textarea_attributes)
        self.appendChild(textarea_tag, "<br>")

    def add_label(self, for_, text=''):
        label = CreateElement("label", **{'for': for_})
        label.text = text
        self.appendChild(label, "<br>")

    def add_button(self, button_type='submit', text='Submit', **attributes):
        button_attributes = {
            'type': button_type,
            **attributes
        }
        button_tag = CreateElement('button', **button_attributes)
        button_tag.appendChild(text)
        self.appendChild(button_tag)

    def __str__(self):
        attribute_string = ' '.join([f'{key}="{value}"' for key, value in self.attributes.items()])
        inner_html = '\n'.join([str(child) for child in self.children])
        return f'<form action="{self.action}" method="{self.method}" {attribute_string}>\n{inner_html}\n</form>'
