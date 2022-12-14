from objects import *

def map_question_to_request(question: Question):
    return (question.title, question.text, question.image, question.position)

# def map_response_to_question(response):
#     question = Question(response.)
