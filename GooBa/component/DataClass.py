class CreateData:
    def __init__(self, *children):
        self.children = list(children)

    def __getitem__(self, item):
        return self.children[item]


# data = CreateData("name", "email")
