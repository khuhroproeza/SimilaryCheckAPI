from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt
import spacy

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")

db = client.SimilarityDB
users = db["Users"]


def UserExist(username):
    if users.find({"Username": username}).count() == 0:
        return False
    else:
        return True


class Register(Resource):
    def post(self):
        postedData = request.get_json()
        username = postedData["username"]
        password = postedData["password"]

        if (UserExist(username)):
            retJson = {
                "status": 301,
                "Message": "Invalid Username"
            }
            return jsonify(retJson)

        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        users.insert(
            {
                "Username": username,
                "Password": hashed_pw,
                "Tokens": 6
            }
        )
        retJson = {
            "status": 200,
            "Message": "You have successfully signed up to the API"
        }

        return jsonify(retJson)


def verifyPw(username, password=None):
    if not UserExist(username):
        return False

    hashed_pw = users.find({
        "Username": username
    })[0]["Password"]

    if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
        return True
    else:
        return False


def countTokens(username):
    tokens = users.find({
        "Username":username
    })[0]["Tokens"]

    return tokens



class Detect(Resource):
    def post(self):
        postedData = request.get_json()
        username = postedData["username"]
        password = postedData["password"]

        text1 = postedData["text1"]
        text2 = postedData["text2"]

        if not UserExist(username):
            retJson = {
                "status": "301",
                "Message": "Invalid Username"
            }
            return jsonify(retJson)

        correct_pw = verifyPw(username, password)

        if not correct_pw:
            retJson = {
                "status": 302,
                "Message": "Invalid Username"
            }
            return jsonify(retJson)

        num_tokens = countTokens(username)

        if num_tokens <= 0:
            retJson = {
                "status": 303,
                "message": "Tokens 0, please refill"
            }
            return jsonify(retJson)

        nlp = spacy.load('en_core_web_sm')

        text1 = nlp(text1)
        text2 = nlp(text2)

        # Defines a number between 0 and 1. 1 being similary 0 being not similar.
        ratio = text1.similarity(text2)

        retJson = {
            "status": 200,
            "Similarity": ratio,
            "Message": "Similarity score calculated Successfully"
        }

        current_tokens = countTokens(username)

        newtokens = current_tokens - 1
        if newtokens < 0:
            newtokens = 0
        users.update({
            "Username": username
        }, {
            "$set": {
                "Tokens": newtokens
            }
        })
        return jsonify(retJson)

class Refill(Resource):
    def post(self):
        postedData = request.get_json()
        username = postedData["username"]
        password = postedData["admin_pw"]

        refill_amount = postedData["refill"]
        if not UserExist(username):
            retJson = {
                "status": 301,
                "Message": "Invalid username"
            }
            return jsonify(retJson)
        correct_pw = "abc123"
        if not password == correct_pw:
            retJson = {
                "status": 304,
                "Message": "Invalid Admin Password"
            }
            return jsonify(retJson)

        #current_tokens = countTokens(username)
        users.update({
            "Username": username
        },{
            "$set": {
                "Tokens": refill_amount #+current_tokens
            }
        })

        retJson = {
            "status": 200,
            "Message": "Refilled Successfully"
        }
        return jsonify(retJson)


api.add_resource(Register, '/register')
api.add_resource(Detect, '/detect')
api.add_resource(Refill, '/refill')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
