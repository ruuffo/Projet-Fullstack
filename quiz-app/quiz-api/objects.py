# Objets

import array
import json

from custom_errors import CustomError


class Answer():
    def __init__(self, text: str, isCorrect: bool):
        self.text = text
        self.isCorrect = isCorrect

    def verifyCreate(self):
        missing_parameters = []
        if self.text == None:
            missing_parameters.append("text")
        if self.isCorrect == None:
            missing_parameters.append("isCorrect")
        if len(missing_parameters) > 0:
            raise CustomError(400, "Missing values for : " + ''.join([str(a) + ", " for a in missing_parameters]))

class Question():
    def __init__(self, title: str, text: str, image: str, position: int, answers: object):
        self.title = title
        self.text = text
        self.image = image
        self.position = position
        self.answers = answers

    def __str__(self):
        return json.dumps(self)

    def verifyCreate(self):
        missing_parameters = []
        if self.text == None:
            missing_parameters.append("text")
        if self.title == None:
            missing_parameters.append("title")
        if self.position == None:
            missing_parameters.append("position")
        if self.image == None:
            missing_parameters.append("image")
        if len(missing_parameters) > 0:
            raise CustomError(400,"Missing values for : "+ ''.join([str(a) + ", " for a in missing_parameters]))
