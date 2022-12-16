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


@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
	return {"size": 0, "scores": []}, 200


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
		authorization = request.headers.get('Authorization').replace("Bearer ","")

		# Lire le token. Si invalide : JwtException
		decode_token(authorization)

		# récupèrer un l'objet json envoyé dans le body de la requète
		json = request.get_json()

		possibleAnswers = json.get("possibleAnswers")

		answers = []
		if possibleAnswers != None:
			for answer in possibleAnswers:
				answers.append(Answer(answer.get("text"), answer.get("isCorrect")))

		# get question
		question = Question(json.get("title"), json.get("text"), json.get("image"), json.get("position"), answers)

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

@app.route('/questions/<int:question_id>', methods=['PUT'])
def PutQuestion(question_id):
	try:
		# Récupérer le token envoyé en paramètre
		authorization = request.headers.get('Authorization').replace("Bearer ","")

		decode_token(authorization)

		# récupèrer un l'objet json envoyé dans le body de la requète
		json = request.get_json()

		possibleAnswers = json.get("possibleAnswers")
		answers = []
		for answer in possibleAnswers :
			answers.append(Answer(answer.get("text"), answer.get("isCorrect")))

		# get question
		question = Question(json.get("title"), json.get("text"), json.get("image"), json.get("position"), answers)

		# register question in database
		PutQuestionSQL(question, question_id)

		#Delete outdated answers
		RemoveAnswersSQL(question_id)

		# register answers in database
		for answer in question.answers:
			PostAnswersSQL(answer, question_id)

		return "OK", 204
	except JwtError as e: # token errors
		return e.message, 401
	except Exception as e:
		return "ERROR : " + str(e)

if __name__ == "__main__":
    app.run()
