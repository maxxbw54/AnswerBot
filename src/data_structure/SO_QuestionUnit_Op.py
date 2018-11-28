class SO_QuestionUnit_Op:
    __name__ = 'SO_QuestionUnit'
    id = -1
    type = -1
    title = ''
    title_op = ''
    desc = ''
    desc_op = ''
    tag = ''

    def __init__(self, id, type, title, title_op, desc, desc_op, tag):
        self.id = id
        self.type = type
        self.title = title
        self.title_op = title_op
        self.desc = desc
        self.desc = desc_op
        self.tag = tag

    def set_id(self, id):
        self.id = id

    def set_type(self, type):
        self.type = type

    def set_title(self, title):
        self.title = title

    def set_desc(self, desc):
        self.desc = desc

    def set_tag(self, tag):
        self.tag = tag

    def get_id(self):
        return self.id

    def get_type(self):
        return self.type

    def get_title(self):
        return self.title

    def get_desc(self):
        return self.desc

    def get_tag(self):
        return self.tag
