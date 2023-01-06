import sqlite3
from custom_errors import CustomError
from objects import *
from mapping import *

# create a connection
def start_connect():
    db_connection = sqlite3.connect("bdd.db")
    db_connection.isolation_level = None
    return db_connection

#region TABLES SQL

def CreateTableQuestionSQL():

    try:
        db_connection = start_connect()
        cur = db_connection.cursor()

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
        db_connection.commit()
        db_connection.close()

    # exception si on arrive pas a créer
    except sqlite3.IntegrityError as e:
        # in case of exception, rollback the transaction
        db_connection.rollback()
        db_connection.close()
        raise CustomError(500, "Cannot create table Question : \n" + str(e))

    except Exception as e:
        db_connection.rollback()
        db_connection.close()
        raise e


def CreateTableAnswerSQL():

    try:

        db_connection = start_connect()
        cur = db_connection.cursor()

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
                Position int not null,
                FOREIGN KEY(Id_Question) REFERENCES Question(Id_Question) ON DELETE CASCADE ON UPDATE CASCADE
            );
            """
        )

        # send the request
        db_connection.commit()
        db_connection.close()

    # exception si on arrive pas a créer
    except sqlite3.IntegrityError as e:
        # in case of exception, rollback the transaction
        db_connection.rollback()
        db_connection.close()
        raise CustomError(500, "Cannot create table Answer : \n" + str(e))

    except Exception as e:
        db_connection.rollback()
        db_connection.close()
        raise e


def CreateTableParticipationSQL():

    try:
        db_connection = start_connect()
        cur = db_connection.cursor()

        # start transaction
        cur.execute("begin")

        # create table Answer
        cur.execute(
            """
            Create TABLE if not EXISTS Participation (
                Id_Participation INTEGER PRIMARY KEY,
                Player_Name varchar(50) not null,
                Score int not null
            );
            """
        )

        # send the request
        db_connection.commit()
        db_connection.close()

    # exception si on arrive pas a créer
    except sqlite3.IntegrityError as e:
        # in case of exception, rollback the transaction
        db_connection.rollback()
        db_connection.close()
        raise CustomError(
            500, "Cannot create table Participation : \n" + str(e))

    except Exception as e:
        db_connection.rollback()
        db_connection.close()
        raise e


def RebuildDBSQL():
    CreateTableQuestionSQL()
    CreateTableAnswerSQL()
    CreateTableParticipationSQL()
#endregion

#region POST

def PostQuestionSQL(question: Question):

    try:

        # QUESTION
        # save the question to db
        question.verifyCreate()

        data = map_question_to_request(question)

        db_connection = start_connect()
        cur = db_connection.cursor()

        # start transaction
        cur.execute("begin")
        insertion_result = cur.execute(
            "insert into Question (Title,Text,Image,Quiz_position) values (?,?,?,?)", data)

        db_connection.commit()
        id = cur.lastrowid
        db_connection.close()

        return id

    # exception si il nous manque des paramètres
    except CustomError as e:
        # in case of exception, rollback the transaction
        db_connection.rollback()
        db_connection.close()
        raise e

    # exception si on essaie de mettre une position qui existe déja
    except sqlite3.IntegrityError as e:
        # in case of exception, rollback the transaction
        db_connection.rollback()
        db_connection.close()
        raise CustomError(400,"Cannot insert Question. The Question with position "+str(question.position)+" already exists.")

    except Exception as e:
        db_connection.rollback()
        db_connection.close()
        raise e

def PostParticipationSQL(participation: Participation):

    try:

        # QUESTION
        # save the question to db
        participation.verifyCreate()

        data = map_participation_to_request(participation)

        db_connection = start_connect()
        cur = db_connection.cursor()

        # start transaction
        cur.execute("begin")

        insertion_result = cur.execute(
            "insert into Participation (Player_Name,Score) values (?,?)", data)

        # send the request
        db_connection.commit()
        id = cur.lastrowid
        db_connection.close()

        return id

    # exception si il nous manque des paramètres
    except CustomError as e:
        # in case of exception, rollback the transaction
        db_connection.rollback()
        db_connection.close()
        raise e

    except Exception as e:
        db_connection.rollback()
        db_connection.close()
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
            "insert into Answer (Text,IsCorrect, Position, Id_Question) values (?,?,?,?)", (data[0], data[1], data[2], question_id))

        # send the request
        db_connection.commit()
        db_connection.close()

    # exception si il nous manque des paramètres
    except CustomError as e:
        db_connection.rollback()
        db_connection.close()
        raise e

    except Exception as e:
        db_connection.rollback()
        db_connection.close()
        raise e
#endregion

#region GET

def GetHighestQuestionPositionSQL():
    try:
        db_connection = start_connect()
        cur = db_connection.cursor()

        # start transaction
        cur.execute("begin")

        cur.execute("SELECT MAX(Quiz_Position) FROM Question")

        db_connection.commit()

        result = cur.fetchone()

        db_connection.close()

        if result == None:
            raise CustomError(
                404, "There are probably no Questions at all in the database")
        return result[0]

    # exception si il nous manque des paramètres
    except CustomError as e:
        db_connection.rollback()
        db_connection.close()
        raise e

    except Exception as e:
        db_connection.rollback()
        db_connection.close()
        raise e

def GetAllParticipationsSQL():
    try:

        db_connection = start_connect()
        cur = db_connection.cursor()

        # start transaction
        cur.execute("begin")

        cur.execute("SELECT * FROM Participation ORDER BY score DESC")

        db_connection.commit()

        result = cur.fetchall()

        db_connection.close()

        if result == None:
            result = []

        allparticipations = []

        for r in result :
            participation = Participation.loadFromDB(r)
            allparticipations.append(participation)

        return allparticipations

    # exception si il nous manque des paramètres
    except CustomError as e:
        db_connection.rollback()
        db_connection.close()
        raise e

    except Exception as e:
        db_connection.rollback()
        db_connection.close()
        raise e


def GetParticipationByIdSQL(part_id: int):
    try:

        db_connection = start_connect()
        cur = db_connection.cursor()

        # start transaction
        cur.execute("begin")

        cur.execute(
            "SELECT * FROM Participation where Id_Participation = ?", (part_id,))

        db_connection.commit()

        result = cur.fetchone()

        db_connection.close()

        if result == None:
            raise CustomError(
                404, "There is no Participation with id = "+str(part_id))

        particiation = Participation.loadFromDB(result)

        return particiation

    # exception si il nous manque des paramètres
    except CustomError as e:
        db_connection.rollback()
        db_connection.close()
        raise e

    except Exception as e:
        db_connection.rollback()
        db_connection.close()
        raise e


def GetParticipationByNameSQL(p_name: str):
    try:

        db_connection = start_connect()
        cur = db_connection.cursor()

        # start transaction
        cur.execute("begin")

        cur.execute(
            "SELECT * FROM Participation where Player_Name = ?", (p_name,))

        db_connection.commit()

        result = cur.fetchone()

        db_connection.close()

        if result == None:
            raise CustomError(
                404, "There is no Participation for player with name = "+str(p_name))

        particiation = Participation.loadFromDB(result)

        return particiation

    # exception si il nous manque des paramètres
    except CustomError as e:
        db_connection.rollback()
        db_connection.close()
        raise e

    except Exception as e:
        db_connection.rollback()
        db_connection.close()
        raise e

def GetQuestionByIdSQL(question_id: int):
    try:
        db_connection = start_connect()
        cur = db_connection.cursor()

        # start transaction
        cur.execute("begin")

        cur.execute("SELECT * FROM Question WHERE Id_Question = ?", (question_id,))

        db_connection.commit()
        result = cur.fetchone()

        db_connection.close()

        if result == None:
            raise CustomError(404, "There is no Question with id = "+str(question_id))

        question = Question.loadFromDB(result)

        return question

    # exception si il nous manque des paramètres
    except CustomError as e:
        db_connection.rollback()
        db_connection.close()
        raise e

    except Exception as e:
        db_connection.rollback()
        db_connection.close()
        raise e

def GetFullQuestionByIdSQL(question_id: int):
    try:
        question = GetQuestionByIdSQL(question_id)
        answers = GetAnswersByQuestionIdSQL(question_id)
        question.answers = answers
        return question
    # exception si il nous manque des paramètres
    except CustomError as e:
        raise e

    except Exception as e:
        raise e

def GetFullQuestionByPositionSQL(position: int):
    try:
        question = GetQuestionByPositionSQL(position)
        answers = GetAnswersByQuestionIdSQL(question.id)
        question.answers = answers
        return question
    # exception si il nous manque des paramètres
    except CustomError as e:
        raise e

    except Exception as e:
        raise e

def GetQuestionByPositionSQL(question_pos: int):
    try:

        db_connection = start_connect()
        cur = db_connection.cursor()

        # start transaction
        cur.execute("begin")

        cur.execute("SELECT * FROM Question WHERE Quiz_Position = ?",
                    (question_pos,))
        db_connection.commit()
        result = cur.fetchone()
        db_connection.close()

        if result == None:
            raise CustomError(
                404, "There is no Question with position = "+str(question_pos))

        question = Question.loadFromDB(result)

        return question

    # exception si il nous manque des paramètres
    except CustomError as e:
        db_connection.rollback()
        db_connection.close()
        raise e

    except Exception as e:
        db_connection.rollback()
        db_connection.close()
        raise e

def GetAnswerByIdSQL(answer_id: int):
    try:
        db_connection = start_connect()
        cur = db_connection.cursor()

        # start transaction
        cur.execute("begin")

        cur.execute("SELECT * FROM Answer WHERE Id_Answer = ?", (answer_id,))

        db_connection.commit()
        result = cur.fetchone()
        db_connection.close()

        if result == None:
            raise CustomError(404, "There is no Answer with id = "+str(answer_id))

        answer = Answer.loadFromDB(result)

        return answer

    # exception si il nous manque des paramètres
    except CustomError as e:
        db_connection.rollback()
        db_connection.close()
        raise e

    except Exception as e:
        db_connection.rollback()
        db_connection.close()
        raise e

def GetAnswersByQuestionIdSQL(question_id: int):
    try:
        db_connection = start_connect()
        cur = db_connection.cursor()

        # start transaction
        cur.execute("begin")

        cur.execute(
            "SELECT * FROM Answer WHERE Id_Question = ?", (question_id,))
        db_connection.commit()
        result = cur.fetchall()
        db_connection.close()

        answers = [Answer.loadFromDB(answer) for answer in result]

        return answers

    # exception si il nous manque des paramètres
    except CustomError as e:
        db_connection.rollback()
        db_connection.close()
        raise e

    except Exception as e:
        db_connection.rollback()
        db_connection.close()
        raise e
#endregion

#region PUT
def PutQuestionSQL(question: Question, question_id: int):

    try:
        # QUESTION
        # save the question to db
        data = map_question_to_request_with_id(question, question_id)

        db_connection = start_connect()
        cur = db_connection.cursor()
        cur.execute("PRAGMA foreign_keys = ON")
        # start transaction
        cur.execute("begin")

        statement = cur.execute("UPDATE Question SET Title = ?, Text = ?, Image = ?, Quiz_position = ? WHERE Id_Question = ?", (data))
        deleted = statement.rowcount

        # send the request
        db_connection.commit()
        db_connection.close()

        if deleted == 0:
            raise CustomError(
                404, "There is no Question with position = "+str(question_id))

    except CustomError as e:
        db_connection.rollback()
        db_connection.close()
        raise e
    except Exception as e:
        # in case of exception, rollback the transaction
        db_connection.rollback()
        db_connection.close()
        raise Exception("Failed to put new question in DB. " + str(e))
#endregion

#region DELETE
def DeleteQuestionSQL(question_id: int):

    try:
        db_connection = start_connect()
        cur = db_connection.cursor()
        cur.execute("PRAGMA foreign_keys = ON")

        # start transaction
        cur.execute("begin")

            #QUESTION
        # delete the question from db
        deleteStatement = cur.execute("DELETE FROM Question WHERE Id_Question = ?", (question_id,))
        count = deleteStatement.rowcount

        # send the request
        db_connection.commit()
        db_connection.close()

        return count

    except Exception as e:
        # in case of exception, rollback the transaction
        db_connection.rollback()
        db_connection.close()
        raise Exception("Failed to remove question with id: "+ str(question_id) +" from DB.\n" + str(e))

def DeleteAllParticipationsSQL():

    try:
        db_connection = start_connect()
        cur = db_connection.cursor()

        # start transaction
        cur.execute("begin")

        # QUESTION
        # delete the question from db
        cur.execute("DELETE FROM Participation")

        # send the request
        db_connection.commit()
        db_connection.close()

    except Exception as e:
        # in case of exception, rollback the transaction
        db_connection.rollback()
        db_connection.close()
        raise Exception("Failed to remove participations from DB.\n" + str(e))

def DeleteAllQuestionsSQL():

    try:
        db_connection = start_connect()
        cur = db_connection.cursor()
        cur.execute("PRAGMA foreign_keys = ON")

        # start transaction
        cur.execute("begin")

        # QUESTION
        # delete the question from db
        cur.execute("DELETE FROM Question")

        # send the request
        db_connection.commit()
        db_connection.close()

    except Exception as e:
        # in case of exception, rollback the transaction
        db_connection.rollback()
        db_connection.close()
        raise Exception("Failed to remove questions from DB.\n" + str(e))

def DeleteAnswersSQL(question_id: int):
    try:
        # ANSWERS
        db_connection = start_connect()
        cur = db_connection.cursor()
        # start transaction
        cur.execute("begin")

        cur.execute("DELETE FROM Answer WHERE Id_Question = ?",(question_id,))

        # send the request
        db_connection.commit()
        db_connection.close()
    except Exception as e:
        # in case of exception, rollback the transaction
        db_connection.rollback()
        db_connection.close()
        raise Exception("Failed to remove old answers to question with id: "+str(question_id)+" from DB. " + str(e))
#endregion