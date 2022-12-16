import sqlite3
from custom_errors import CustomError
from objects import *
from mapping import *

# create a connection
def start_connect():
    db_connection = sqlite3.connect("bdd.db")
    db_connection.isolation_level = None
    return db_connection


def PostQuestionSQL(question: Question):
    db_connection = start_connect()
    cur = db_connection.cursor()


    print("lala\n")

    try:

        # start transaction
        cur.execute("begin")

            #QUESTION
        # save the question to db
        missing_parameters = []
        if question.text == None:
            missing_parameters.append("text")
        if question.title == None:
            missing_parameters.append("title")
        if question.position == None:
            missing_parameters.append("position")
        if question.image == None:
            missing_parameters.append("image")
        if len(missing_parameters) > 0:
            raise CustomError(400,"Missing values for : "+ ''.join([str(a) + ", " for a in missing_parameters]))

        data = map_question_to_request(question)
        insertion_result = cur.execute(
            "insert into Question (Title,Text,Image,Quiz_position) values (?,?,?,?)", data)
        # send the request
        cur.execute("commit")
        cur.close()

        return cur.lastrowid

    # exception si il nous manque des paramètres
    except CustomError as e:
        raise e

    # exception si on essaie de mettre une position qui existe déja
    except sqlite3.IntegrityError as e:
        # in case of exception, rollback the transaction
        cur.execute('rollback')
        cur.close()
        raise CustomError(400,"Cannot insert Question. The Question with position "+str(question.position)+" already exists.")


def PostAnswersSQL(answer: Answer, question_id: int):
    # ANSWERS
    db_connection = start_connect()
    cur = db_connection.cursor()
    try:
        cur = db_connection.cursor()
        # start transaction
        cur.execute("begin")

        missing_parameters = []

        if answer.text == None:
            missing_parameters.append("text")
        if answer.isCorrect == None:
            missing_parameters.append("isCorrect")
        if len(missing_parameters) > 0 :
            raise CustomError(400,"Missing values for : "+ ''.join([str(a) + ", " for a in missing_parameters]))

        data = map_answer_to_request(answer)
        insertion_result = cur.execute(
            "insert into Answer (Text,IsCorrect,Id_Question) values (?,?,?)", (data[0], data[1], question_id))

        # send the request
        cur.execute("commit")
        cur.close()

    # exception si il nous manque des paramètres
    except CustomError as e:
        cur.execute('rollback')
        cur.close()
        raise e
