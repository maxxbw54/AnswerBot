class SO_QuestionUnit:
    __name__ = 'SO_QuestionUnit'
    id = ''
    type = ''
    title = ''
    title_NO_SW = ''
    title_NO_SW_Stem = ''
    tag = ''

    # def __init__(self, id, type, title, tag):
    #     self.id = id
    #     self.type = type
    #     self.title = title
    #     self.tag = tag

    def __init__(self, id, type, title, title_NO_SW, title_NO_SW_Stem, tag):
        self.id = id
        self.type = type
        self.title = title
        self.title_NO_SW = title_NO_SW
        self.title_NO_SW_Stem = title_NO_SW_Stem
        self.tag = tag

    def set_id(self, id):
        self.id = id

    def set_type(self, type):
        self.type = type

    def set_title(self, title):
        self.title = title

    def set_tag(self, tag):
        self.tag = tag

    def get_id(self):
        return self.id

    def get_type(self):
        return self.type

    def get_title(self):
        return self.title

    def get_tag(self):
        return self.tag
