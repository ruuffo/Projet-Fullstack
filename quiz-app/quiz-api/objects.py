# Objets

class Answer():
    def __init__(self, name: str):
        self.name = name

class Question():
    def __init__(self, title: str, text: str, image: str, position: int):
        self.title = title
        self.text = text
        self.image = image
        self.position = position