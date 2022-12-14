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

        # save the question to db
        data = map_question_to_request(question)
        insertion_result = cur.execute(
            "insert into Question (Title,Text,Image,Quiz_position) values (?,?,?,?)", data)

        # send the request
        cur.execute("commit")

    except Exception as e:
        # in case of exception, rollback the transaction
        cur.execute('rollback')
        raise Exception("Failed to insert in DB. " + str(e))
