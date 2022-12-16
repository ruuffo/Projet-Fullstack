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

    try:

        # start transaction
        cur.execute("begin")

            #QUESTION
        # save the question to db
        question.verifyCreate()

        data = map_question_to_request(question)
        insertion_result = cur.execute(
            "insert into Question (Title,Text,Image,Quiz_position) values (?,?,?,?)", data)

        # send the request
        cur.execute("commit")
        cur.close()

        return cur.lastrowid

    # exception si il nous manque des paramètres
    except CustomError as e:
        # in case of exception, rollback the transaction
        cur.execute('rollback')
        cur.close()
        raise e

    # exception si on essaie de mettre une position qui existe déja
    except sqlite3.IntegrityError as e:
        # in case of exception, rollback the transaction
        cur.execute('rollback')
        cur.close()
        raise CustomError(400,"Cannot insert Question. The Question with position "+str(question.position)+" already exists.")

    except Exception as e:
        cur.execute('rollback')
        cur.close()
        raise e


def PostAnswersSQL(answer: Answer, question_id: int):
    # ANSWERS
    db_connection = start_connect()
    cur = db_connection.cursor()
    try:
        cur = db_connection.cursor()
        # start transaction
        cur.execute("begin")

        answer.verifyCreate()

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

    except Exception as e:
        cur.execute('rollback')
        cur.close()
        raise e


def GetQuestionByIdSQL(question_id: int):
    db_connection = start_connect()
    cur = db_connection.cursor()
    try:
        cur = db_connection.cursor()
        # start transaction
        cur.execute("begin")

        cur.execute("SELECT * FROM Question WHERE Id_Question = ?", (question_id,))
        result = cur.fetchone()

        if result == None:
            raise CustomError(404, "There is no Question with id = "+str(question_id))

        # send the request
        cur.close()
        return result

    # exception si il nous manque des paramètres
    except CustomError as e:
        cur.close()
        raise e

    except Exception as e:
        cur.close()
        raise e




def PutQuestionSQL(question: Question, question_id: int):
    db_connection = start_connect()
    cur = db_connection.cursor()

    try:

        # start transaction
        cur.execute("begin")

            #QUESTION
        # save the question to db
        data = map_question_to_request_with_id(question,question_id)
        cur.execute("UPDATE Question SET Title = ?, Text = ?, Image = ?, Quiz_position = ? WHERE Id_Question = ?", (data))
        # send the request
        cur.execute("commit")
        cur.close()

    except Exception as e:
        # in case of exception, rollback the transaction
        cur.execute('rollback')
        cur.close()
        raise Exception("Failed to update DB. " + str(e))


def RemoveAnswersSQL(question_id: int):
    # ANSWERS
    db_connection = start_connect()
    cur = db_connection.cursor()
    try:
        cur = db_connection.cursor()
        # start transaction
        cur.execute("begin")

        cur.execute("DELETE FROM answer WHERE Id_Question = ?",(question_id,))

        # send the request
        cur.execute("commit")
        cur.close()
    except Exception as e:
        # in case of exception, rollback the transaction
        cur.execute('rollback')
        cur.close()
        raise Exception("Failed to remove old answers in DB. " + str(e))
