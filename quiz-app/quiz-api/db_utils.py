import sqlite3
from custom_errors import CustomError
from objects import *
from mapping import *

# create a connection
def start_connect():
    db_connection = sqlite3.connect("bdd.db")
    db_connection.isolation_level = None
    return db_connection

#region POST
def CreateTableQuestionSQL():
    db_connection = start_connect()
    cur = db_connection.cursor()

    try:

        # start transaction
        cur.execute("begin")

        # create table Question
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS Question(
                Id_Question INTEGER PRIMARY KEY,
                Title varchar(50) not null,
                Text varchar(50) not null,
                Image varchar(100) not null,
                Quiz_Position int not null
            );
            """
        )

        # send the request
        cur.execute("commit")
        cur.close()

    # exception si on arrive pas a créer
    except sqlite3.IntegrityError as e:
        # in case of exception, rollback the transaction
        cur.execute('rollback')
        cur.close()
        raise CustomError(500, "Cannot create table Question : \n" + str(e))

    except Exception as e:
        cur.execute('rollback')
        cur.close()
        raise e


def CreateTableAnswerSQL():
    db_connection = start_connect()
    cur = db_connection.cursor()

    try:

        # start transaction
        cur.execute("begin")

        # create table Answer
        cur.execute(
            """
            Create TABLE if not EXISTS Answer (
                Id_Answer INTEGER PRIMARY KEY,
                Id_Question int not null,
                Text varchar(50) not null,
                IsCorrect BOOLEAN not null check(IsCorrect in (0,1)),
                FOREIGN KEY(Id_Question) REFERENCES Question(Id_Question)
            );
            """
        )

        # send the request
        cur.execute("commit")
        cur.close()

    # exception si on arrive pas a créer
    except sqlite3.IntegrityError as e:
        # in case of exception, rollback the transaction
        cur.execute('rollback')
        cur.close()
        raise CustomError(500, "Cannot create table Answer : \n" + str(e))

    except Exception as e:
        cur.execute('rollback')
        cur.close()
        raise e


def RebuildDBSQL():
    CreateTableQuestionSQL()
    CreateTableAnswerSQL()


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
#endregion

#region GET
def GetQuestionByIdSQL(question_id: int):
    db_connection = start_connect()
    cur = db_connection.cursor()
    try:
        cur = db_connection.cursor()
        # start transaction
        cur.execute("begin")

        cur.execute("SELECT * FROM Question WHERE Id_Question = ?", (question_id,))
        result = cur.fetchone()
        print(result)

        if result == None:
            raise CustomError(404, "There is no Question with id = "+str(question_id))

        question = Question.loadFromDB(result)

        # send the request
        cur.close()
        return question

    # exception si il nous manque des paramètres
    except CustomError as e:
        cur.close()
        raise e

    except Exception as e:
        cur.close()
        raise e


def GetQuestionByPositionSQL(question_pos: int):
    db_connection = start_connect()
    cur = db_connection.cursor()
    try:
        cur = db_connection.cursor()
        # start transaction
        cur.execute("begin")

        cur.execute("SELECT * FROM Question WHERE Quiz_Position = ?",
                    (question_pos,))
        result = cur.fetchone()
        print(result)

        if result == None:
            raise CustomError(
                404, "There is no Question with position = "+str(question_pos))

        question = Question.loadFromDB(result)

        # send the request
        cur.close()
        return question

    # exception si il nous manque des paramètres
    except CustomError as e:
        cur.close()
        raise e

    except Exception as e:
        cur.close()
        raise e


def GetAnswersByQuestionIdSQL(question_id: int):
    db_connection = start_connect()
    cur = db_connection.cursor()
    try:
        cur = db_connection.cursor()
        # start transaction
        cur.execute("begin")

        cur.execute(
            "SELECT * FROM Answer WHERE Id_Question = ?", (question_id,))
        result = cur.fetchall()

        answers = [Answer.loadFromDB(answer) for answer in result]

        # send the request
        cur.close()
        return answers

    # exception si il nous manque des paramètres
    except CustomError as e:
        cur.close()
        raise e

    except Exception as e:
        cur.close()
        raise e
#endregion

#region PUT
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

    except CustomError as e:
        cur.close()
        raise e
    except Exception as e:
        # in case of exception, rollback the transaction
        cur.execute('rollback')
        cur.close()
        raise Exception("Failed to put new question in DB. " + str(e))
#endregion

#region DELETE
def DeleteQuestionSQL(question_id: int):
    db_connection = start_connect()
    cur = db_connection.cursor()

    try:
        # start transaction
        cur.execute("begin")

            #QUESTION
        # delete the question from db
        cur.execute("DELETE FROM Question WHERE Id_Question = ?", (question_id,))

        # send the request
        cur.execute("commit")

        cur.close()

    except Exception as e:
        # in case of exception, rollback the transaction
        cur.execute('rollback')
        cur.close()
        raise Exception("Failed to remove question with id: "+ str(question_id) +" from DB.\n" + str(e))


def DeleteAnswersSQL(question_id: int):
    # ANSWERS
    db_connection = start_connect()
    cur = db_connection.cursor()
    try:
        cur = db_connection.cursor()
        # start transaction
        cur.execute("begin")

        cur.execute("DELETE FROM Answer WHERE Id_Question = ?",(question_id,))

        # send the request
        cur.execute("commit")
        cur.close()
    except Exception as e:
        # in case of exception, rollback the transaction
        cur.execute('rollback')
        cur.close()
        raise Exception("Failed to remove old answers to question with id: "+str(question_id)+" from DB. " + str(e))
#endregion