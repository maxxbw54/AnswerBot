class SO_Ans:
    __slots__ = 'id', 'body', 'score', 'parent_id', 'tag'

    def __init__(self, id, body, score, parent_id, tag):
        self.id = id
        self.body = body
        self.score = score
        self.parent_id = parent_id
        self.tag = tag
