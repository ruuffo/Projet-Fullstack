from sqlite3 import IntegrityError, OperationalError
from flask import Flask, request
from flask_cors import CORS
from jwt_utils import *
from objects import *
from db_utils import *
from custom_errors import *

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
	x = 'world'
	return f"Hello, {x}"

#region GET

@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
	return {"size": 0, "scores": []}, 200


@app.route('/questions/<int:question_id>', methods=['GET'])
def GetQuestionById(question_id):
	try:
		# Récupérer le token envoyé en paramètre
		authorization = request.headers.get('Authorization')
		decode_token(authorization)

		# get question in database
		question = GetQuestionByIdSQL(question_id)
		answers = GetAnswersByQuestionIdSQL(question_id)
		question.answers = answers

		return jsonify(question.toJSON()), 200
	except JwtError as e:  # token errors
		return e.message, 401
	except CustomError as e:
		return e.message, e.code
	except Exception as e:
		return "ERROR : " + str(e), e.args[0]


@app.route('/questions', methods=['GET'])
def GetQuestionByPosition():
	try:
		# Récupérer le token envoyé en paramètre
		authorization = request.headers.get('Authorization')
		decode_token(authorization)

		# get position
		question_pos = request.args['position']
		if (question_pos == None):
			raise CustomError(404, "Missing position")

		# get question in database
		question = GetQuestionByPositionSQL(question_pos)
		answers = GetAnswersByQuestionIdSQL(question.id)
		question.answers = answers

		return jsonify(question.toJSON()), 200
	except JwtError as e:  # token errors
		return e.message, 401
	except CustomError as e:
		return e.message, e.code
	except Exception as e:
		return "ERROR : " + str(e), e.args[0]

# endregion

#region POST
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
				answers.append(Answer(None,answer.get("text"), answer.get("isCorrect")))

		# get question
		question = Question(None, json.get("title"), json.get("text"), json.get("image"), json.get("position"), answers)

		# register question in database
		id_question = PostQuestionSQL(question)

        # register answers in database
		for answer in question.answers:
			PostAnswersSQL(answer, id_question)

		return {"id":id_question}, 200
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
			answers.append(Answer(None, answer.get("text"), answer.get("isCorrect")))

		# get question
		question = Question(None,json.get("title"), json.get("text"), json.get("image"), json.get("position"), answers)

		# register question in database
		PutQuestionSQL(question, question_id)

		#Delete outdated answers
		DeleteAnswersSQL(question_id)

		# register answers in database
		for answer in question.answers:
			PostAnswersSQL(answer, question_id)

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
		DeleteQuestionSQL(question_id)

		# Delete outdated answers
		AnswersSQL(question_id)

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
