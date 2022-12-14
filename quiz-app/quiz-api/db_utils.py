import sqlite3
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
        data = map_question_to_request(question)
        insertion_result = cur.execute(
            "insert into Question (Title,Text,Image,Quiz_position) values (?,?,?,?)", data)
        # send the request
        cur.execute("commit")
        cur.close()

        return cur.lastrowid

    except Exception as e:
        # in case of exception, rollback the transaction
        cur.execute('rollback')
        cur.close()
        raise Exception("Failed to insert in DB. " + str(e))


def PostAnswersSQL(answer: Answer, question_id: int):
    # ANSWERS
    db_connection = start_connect()
    cur = db_connection.cursor()
    try:
        cur = db_connection.cursor()
        # start transaction
        cur.execute("begin")

        data = map_answer_to_request(answer)
        insertion_result = cur.execute(
            "insert into Answer (Text,IsCorrect,Id_Question) values (?,?,?)", (data[0], data[1], question_id))

        # send the request
        cur.execute("commit")
        cur.close()
    except Exception as e:
        # in case of exception, rollback the transaction
        cur.execute('rollback')
        cur.close()
        raise Exception("Failed to insert in DB. " + str(e))
