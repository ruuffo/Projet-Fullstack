from objects import *


def map_question_to_request(question: Question):
    return (question.title, question.text, question.image, question.position)

def map_question_to_request_with_id(question: Question, question_id):
    return (question.title, question.text, question.image, question.position, question_id)


def map_answer_to_request(answer: Answer):
    return (answer.text, answer.isCorrect, answer.position)

# def map_response_to_question(response):
#     question = Question(response.)
