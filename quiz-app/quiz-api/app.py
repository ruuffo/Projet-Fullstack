from sqlite3 import IntegrityError, OperationalError
from flask import Flask, request, jsonify
from flask_cors import CORS
from jwt_utils import *
from objects import *
from db_utils import *
from custom_errors import *
from objects import *

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
	x = 'world'
	return f"Hello, {x}"

#region GET

@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
    participants = GetAllParticipationsSQL()
    scores = []
    for p in participants:
        scores.append({"playerName": p.playerName, "score":p.score})

    size = GetHighestQuestionPositionSQL()
    if size == None:
        size = 0

    #scores = sorted(scores, key = lambda s: s["score"], reverse=True)

    return {"size": size, "scores": scores}, 200


@app.route('/questions/<int:question_id>', methods=['GET'])
def GetQuestionById(question_id):
	try:
		# Récupérer le token envoyé en paramètre /////
		#authorization = request.headers.get('Authorization')
		#decode_token(authorization)

		# get question in database
		question = GetFullQuestionByIdSQL(question_id)

		return question.toJSON(), 200
	except JwtError as e:  # token errors
		return e.message, 401
	except CustomError as e:
		return e.message, e.code
	except Exception as e:
		return "ERROR : " + str(e), e.args[0]


@app.route('/questions', methods=['GET'])
def GetQuestionByPosition():
	try:
		# Récupérer le token envoyé en paramètre /////
		#authorization = request.headers.get('Authorization')
		# decode_token(authorization)

		# get position
		question_pos = request.args['position']
		if (question_pos == None):
			raise CustomError(404, "Missing position")

		# get question in database
		question = GetFullQuestionByPositionSQL(question_pos)

		return question.toJSON(), 200
	except JwtError as e:  # token errors
		return e.message, 401
	except CustomError as e:
		return e.message, e.code
	except Exception as e:
		return "ERROR : " + str(e), e.args[0]


@app.route('/questions/all', methods=['GET'])
def GetAllQuestions():
	try:
		# get question in database
		allquestions = GetAllQuestionsSQL()

		qlist = []
		for q in allquestions:
			qlist.append(q.toJSON())

		return qlist, 200

	except CustomError as e:
		return e.message, e.code
	except Exception as e:
		return "ERROR : " + str(e), e.args[0]

@app.route('/participations', methods=['GET'])
def GetParticipationByName():
	try:
		# Récupérer le token envoyé en paramètre /////
		#authorization = request.headers.get('Authorization')
		# decode_token(authorization)

		# get position
		p_name = request.args['name']
		if (p_name == None):
			raise CustomError(404, "Missing player name")

		# get question in database
		participation = GetParticipationByNameSQL(p_name)

		return participation.toJSON(), 200
	except JwtError as e:  # token errors
		return e.message, 401
	except CustomError as e:
		return e.message, e.code
	except Exception as e:
		return "ERROR : " + str(e), e.args[0]


# endregion

# region POST

@app.route('/login', methods=['POST'])
def Login():
	try:
		payload = request.get_json()
		password = payload.get("password")
		if (password == "flask2023"):
			token = build_token()
			return {"token": token}, 200
		else:
			raise CustomError(401, "Unauthorized - wrong password used : " + password)
	except CustomError as e:
		return str(e), e.code


@app.route('/participations', methods=['POST'])
def PostParticipation():
	try:

		# récupèrer un l'objet json envoyé dans le body de la requète
		json = request.get_json()

		answers_list = [a for a in json.get("answers")]
		if (len(answers_list) != GetHighestQuestionPositionSQL()):
			raise CustomError(400, "The number of answers differs from the number of Questions")

		score = 0
		print("post")

		for question_num in range(1, len(answers_list) + 1):
			question = GetFullQuestionByPositionSQL(question_num)
			if question.answerIsTrueInPosition(answers_list[question_num - 1]):
				score += 1

		participation = Participation(None, json.get("playerName"), score)

		# register participation in database
		print("avant post")
		id_participation = PostParticipationSQL(participation)
		player = GetParticipationByIdSQL(id_participation)

		return player.toJSON(), 200
	except JwtError as e:  # token errors
		return e.message, 401
	except CustomError as e:
		return str(e), e.code
	except Exception as e:
		return "ERROR : " + str(e), e.args[0]


@app.route('/questions', methods=['POST'])
def PostQuestion():
	try:
		# Récupérer le token envoyé en paramètre
		authorization = request.headers.get('Authorization')

		# Lire le token. Si invalide : JwtException
		decode_token(authorization)

		# récupèrer un l'objet json envoyé dans le body de la requète
		json = request.get_json()

		possibleAnswers = json.get("possibleAnswers")

		answers = []
		if possibleAnswers != None:
			for answer in possibleAnswers:
				answers.append(Answer(None,answer.get("text"), answer.get("isCorrect"), None))

		# get complete question
		question = Question(None, json.get("title"), json.get("text"), json.get("image"), json.get("position"), answers)

		# check if already a question at position
		try:
			testq = GetQuestionByPositionSQL(question.position)

			#then increase all equal and superior positions by 1
			IncreasePositionsByOneSQL(testq.position, None)
		except Exception:
			#if no question in position ( error ), do nothing more
			pass

		finally:
			# register question in database
			id_question = PostFullQuestionSQL(question)

			question = GetFullQuestionByIdSQL(id_question)

			return question.toJSON(), 200
	except JwtError as e: # token errors
		return e.message, 401
	except CustomError as e:
		return str(e), e.code
	except Exception as e:
		return "ERROR : " + str(e), e.args[0]


@app.route('/rebuild-db', methods=['POST'])
def RebuildDB():
	try:
		# Récupérer le token envoyé en paramètre
		authorization = request.headers.get('Authorization')

		# Lire le token. Si invalide : JwtException
		decode_token(authorization)

		# execute le script pour rebuild la DB
		RebuildDBSQL()

		return "Ok", 200
	except JwtError as e:  # token errors
		return e.message, 401
	except CustomError as e:
		return str(e), e.code
	except Exception as e:
		return "ERROR : " + str(e), e.args[0]

#endregion

#region PUT
@app.route('/questions/<int:question_id>', methods=['PUT'])
def UpdateQuestion(question_id):
	try:
		# Récupérer le token envoyé en paramètre
		authorization = request.headers.get('Authorization')

		decode_token(authorization)

		# récupèrer un l'objet json envoyé dans le body de la requète
		json = request.get_json()

		possibleAnswers = json.get("possibleAnswers")
		answers = []
		for answer in possibleAnswers :
			answers.append(Answer(None, answer.get("text"), answer.get("isCorrect"), None))

		# get question
		question = Question(None,json.get("title"), json.get("text"), json.get("image"), json.get("position"), answers)

		try:
			# try to get existing question at that position
			testq = GetFullQuestionByPositionSQL(question.position)

			try:
				# get current question to get current position
				currentq = GetFullQuestionByIdSQL(question_id)

				currentPos = currentq.position
				aimedPos = testq.position

				if currentPos < aimedPos:
					DecreasePositionsByOneSQL(currentPos, aimedPos)
				else:
					IncreasePositionsByOneSQL(aimedPos, currentPos)

			except Exception as e:
				# if no such question, or error post, raise error
				raise e
		except Exception as e:
			# if no question at that position, or errors, just continue
			pass

		finally:

			# register question in database
			PutFullQuestionSQL(question, question_id)

			return "OK", 204
	except JwtError as e: # token errors
		return e.message, 401
	except CustomError as e:
		return e.message, e.code
	except Exception as e:
		return "ERROR : " + str(e), e.args[0]
#endregion

#region DELETE

@app.route('/questions/<int:question_id>', methods=['DELETE'])
def DeleteQuestion(question_id):
	try:
		# Récupérer le token envoyé en paramètre
		authorization = request.headers.get('Authorization')
		decode_token(authorization)

		# register question in database
		question = GetQuestionByIdSQL(question_id)
		count = DeleteQuestionSQL(question_id)
		if (count == 0):
			raise CustomError(404, "No question with id : "+str(question_id))

		DecreasePositionsByOneSQL(question.position, None)

		return "OK", 204
	except JwtError as e:  # token errors
		return e.message, 401
	except CustomError as e:
		return e.message, e.code
	except Exception as e:
		return "ERROR : " + str(e), e.args[0]


@app.route('/questions/all', methods=['DELETE'])
def DeleteAllQuestions():
	try:
		# Récupérer le token envoyé en paramètre
		authorization = request.headers.get('Authorization')
		decode_token(authorization)

		# register question in database
		DeleteAllQuestionsSQL()

		return "OK", 204
	except JwtError as e:  # token errors
		return e.message, 401
	except CustomError as e:
		return e.message, e.code
	except Exception as e:
		return "ERROR : " + str(e), e.args[0]


@app.route('/participations/all', methods=['DELETE'])
def DeleteAllParticipations():
	try:
		# Récupérer le token envoyé en paramètre
		authorization = request.headers.get('Authorization')
		decode_token(authorization)

		# register question in database
		DeleteAllParticipationsSQL()

		return "OK", 204
	except JwtError as e:  # token errors
		return e.message, 401
	except CustomError as e:
		return e.message, e.code
	except Exception as e:
		return "ERROR : " + str(e), e.args[0]
#endregion

if __name__ == "__main__":
    app.run()
