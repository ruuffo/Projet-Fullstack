# Objets

import array
import json

from flask import jsonify

from custom_errors import CustomError


class Answer():
    def __init__(self, id: int, text: str, isCorrect: bool):
        self.id = id
        self.text = text
        self.isCorrect = isCorrect

    def toJSON(self):
        return {
            "id": self.id,
            "text": self.text,
            "isCorrect": bool(self.isCorrect),
        }

    def __str__(self):
        return jsonify(self.toJSON())

    def verifyCreate(self):
        missing_parameters = []
        if self.text == None:
            missing_parameters.append("text")
        if self.isCorrect == None:
            missing_parameters.append("isCorrect")
        if len(missing_parameters) > 0:
            raise CustomError(400, "Missing values for : " + ''.join([str(a) + ", " for a in missing_parameters]))

    def loadFromDB(dbResult : object):
        return Answer(dbResult[0], dbResult[2], dbResult[3])

class Question():
    def __init__(self, id: int, title: str, text: str, image: str, position: int, answers: object):
        self.id = id
        self.title = title
        self.text = text
        self.image = image
        self.position = position
        self.answers = answers

    def toJSON(self):
        return {
            "id": self.id,
            "title":self.title,
            "text":self.text,
            "image": self.image,
            "position": self.position,
            "possibleAnswers":[answer.toJSON() for answer in self.answers]
        }

    def __str__(self):
        return jsonify(self.toJSON())

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

    def loadFromDB(dbResult: object):
        return Question(dbResult[0], dbResult[1], dbResult[2], dbResult[3], dbResult[4], None)
