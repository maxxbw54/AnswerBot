class SO_AnswerUnit:
    __name__ = 'SO_AnswerUnit'
    id = -1
    type = -1
    score = -1
    desc = ''

    def __init__(self, id, type, score, desc):
        self.id = id
        self.type = type
        self.score = score
        self.desc = desc

    def set_id(self, id):
        self.id = id

    def set_type(self, type):
        self.type = type

    def set_score(self, score):
        self.score = score

    def set_desc(self, desc):
        self.desc = desc

    def get_id(self):
        return self.id

    def get_type(self):
        return self.type

    def get_score(self):
        return self.score

    def get_desc(self):
        return self.desc
