# Objets

import array


class Answer():
    def __init__(self, name: str, isCorrect: bool):
        self.name = name
        self.isCorrect = isCorrect

class Question():
    def __init__(self, title: str, text: str, image: str, position: int, answers: object):
        self.title = title
        self.text = text
        self.image = image
        self.position = position
        self.answers = answers