class Selectors:
    def __init__(self, ):
        self.id = None
        self.class_ = None
        self.query = None

    def IdSelector(self, id):
        self.id = id

    def ClassSelector(self, class_):
        self.class_ = class_

    def QuerySelector(self, query):
        self.query = query

