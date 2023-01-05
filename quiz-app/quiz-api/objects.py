# Objets

import array
import json

from custom_errors import CustomError


class Answer():
    def __init__(self, id: int, text: str, isCorrect: bool, position: int):
        self.id = id
        self.text = text
        self.isCorrect = isCorrect
        self.position = position

    def toJSON(self):
        return {
            "id": self.id,
            "text": self.text,
            "isCorrect": bool(self.isCorrect),
            "position": self.position
        }

    def verifyCreate(self):
        missing_parameters = []
        if self.text == None:
            missing_parameters.append("text")
        if self.isCorrect == None:
            missing_parameters.append("isCorrect")
        if self.position == None:
            missing_parameters.append("position")
        if len(missing_parameters) > 0:
            raise CustomError(400, "Missing values for : " + ''.join([str(a) + ", " for a in missing_parameters]))

    def loadFromDB(dbResult : object):
        return Answer(dbResult[0], dbResult[2], dbResult[3], dbResult[4])

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

    def getAnswerInPosition(self, pos: int):
        if pos < 1:
            raise CustomError(400, "An answer is always at least in position 1 : " + str(pos))
        if pos > len(self.answers):
            raise CustomError(400, "There is no answer of that position : " + str(pos))

        return self.answers[pos - 1]

    def answerIsTrueInPosition(self, pos: int):
        return self.getAnswerInPosition(pos).isCorrect

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


class Participation() :
    def __init__(self, id: int, playerName: str, score: int):
        self.id = id
        self.playerName = playerName
        self.score = score

    def toJSON(self):
        return {
            "id": self.id,
            "playerName": self.playerName,
            "score": self.score
        }

    def verifyCreate(self):
        missing_parameters = []
        if self.playerName == None:
            missing_parameters.append("playerName")
        if self.score == None:
            missing_parameters.append("score")
        if len(missing_parameters) > 0:
            raise CustomError(400,"Missing values for : "+ ''.join([str(a) + ", " for a in missing_parameters]))


    def loadFromDB(dbResult: object):
        return Participation(dbResult[0], dbResult[1], dbResult[2])
