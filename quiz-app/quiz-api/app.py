from flask import Flask, request
from flask_cors import CORS
from jwt_utils import *
from objects import *
from db_utils import *

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
	payload = request.get_json()
	if (payload.get("password") == "flask2023"):
		token = build_token()
		print(token)
		return {"token":token}, 200
	else:
		return "Unauthorized", 401


@app.route('/questions', methods=['POST'])
def PostQuestion():
	try:
		# Récupérer le token envoyé en paramètre
		authorization = request.headers.get('Authorization').replace("Bearer ","")
		print(authorization)

		#if (authorization == None):
		decode_token(authorization)
			#return "Unauthorized", 401

		# récupèrer un l'objet json envoyé dans le body de la requète
		json = request.get_json()

		question = Question(json.get("title"), json.get("text"), json.get("image"), json.get("position"))
		print(question.title)
		print(question.text)
		print(question.image)
		print(question.position)

		PostQuestionSQL(question)
		return "OK", 200
	except JwtError as e: # token errors
		return e.message, 401
	except Exception as e:
		return "NOPE", 500


if __name__ == "__main__":
    app.run()
