# form

class Form:
    def __init__(self):
        self.fields = []
        self.action = None
        self.method = None

    def addField(self, field):
        self.fields.append(str(field))

    def addFields(self, *fields):
        for field in fields:
            self.fields.append(str(field))

    def __str__(self):
        form = f'<form action="{self.action}" method="{self.method}">\n'
        for field in self.fields:
            form += str(field) + "\n"
        form += "</form>\n"
        return form


class InputField:
    def __init__(self, name, **attributes):
        self.name = name
        self.type = "text"
        self.label = None
        self.attributes = attributes

    def __str__(self):
        input_ = ""  # Define input_ variable here
        attribute_string = ' '.join([f'{key}="{value}"' for key, value in self.attributes.items()])

        if 'className' in self.attributes:
            attribute_string = attribute_string.replace('className', 'class')

        if '\n' in self.name:
            self.name = self.name.replace('\n', '')
            input_ = f'<input type="{self.type}" name="{self.name}"><br>\n'

        else:
            input_ = f'<input type="{self.type}" name="{self.name}">\n'

        if self.label:
            input_ = str(self.label) + input_

        elif attribute_string:
            input_ = f'<input type="{self.type}" name="{self.name} {attribute_string}">'

        return input_
