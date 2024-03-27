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


