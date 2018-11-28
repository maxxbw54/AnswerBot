class SO_AnswerUnit_Op:
    __name__ = 'SO_AnswerUnit'
    id = -1
    type = -1
    score = -1
    desc = ''
    parentId = -1

    def __init__(self, id, type, score, desc, desc_op, parentId):
        self.id = id
        self.type = type
        self.score = score
        self.desc = desc
        self.desc_op = desc_op
        self.parentId = parentId

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
