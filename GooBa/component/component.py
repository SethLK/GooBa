class Element:
    def __init__(self, tag, **attributes):
        self.tag = tag
        self.attributes = attributes
        self.text = None

    # def set_text(self, text):
    #     self.text = text

    def __str__(self):
        attribute_string = ' '.join([f'{key}="{value}"' for key, value in self.attributes.items()])
        if self.text is not None:
            return f'<{self.tag} {attribute_string}>{self.text}</{self.tag}>'
        else:
            return f'<{self.tag} {attribute_string}></{self.tag}>'

    def __add__(self, other):
        if isinstance(other, Element):
            return self.__str__() + other.__str__()
        else:
            return self.__str__() + str(other)


class Image:
    def __init__(self, src, alt=None, **attributes):
        self.src = src
        self.alt = alt
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
