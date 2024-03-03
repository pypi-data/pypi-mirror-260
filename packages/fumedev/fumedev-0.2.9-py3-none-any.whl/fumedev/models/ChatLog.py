class ChatLog:
    def __init__(self, id, role, content, finished=True):
        self.id = id
        self.role = role
        self.content = content
        self.finished = finished