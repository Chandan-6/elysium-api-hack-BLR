import os
from api import utils, model
from mongo import conversion

import pymongo.collection

from encryption import encryption

from dotenv import load_dotenv
from flask import Flask, g, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin

app = Flask(__name__)

CORS(app, origins=["*"])
app.config['CORS_HEADERS'] = 'Content-Type'

load_dotenv()

app.config[
    'MONGO_DBNAME'] = f"mongodb+srv://{os.environ.get('USERNAME')}:{os.environ.get('PASSWORD')}@cluster0.qv3wn6u.mongodb.net/Data?retryWrites=true&w=majority&appName=Cluster0"

mongo = PyMongo(app)
db = mongo.db


@app.route("/api")
def hello_world():
    return "<p>Hello World!</p>"


@app.route("/api/register", methods=[POST])
@cross_origin()
def register():
    data = request.get_json()  # {Name, Email, Password, Type}
    collection: pymongo.collection.Collection = db.auth
    count = collection.count()
    salt = encryption.sha256_encrypt(data['password'])
    final = {'ID': count + 1, 'Name': data['name'].lower(), 'Email': data['email'].lower(), 'Hash': salt,
             'Type': data['category'].lower}
    if not utils.signed_up(name=data['name'].lower(), email=data['email'].lower(), category=data['category'].lower()):
        collection.insert_one(final)
        return jsonify({'message': 'Registered Successfully!', 'ID': count+1, 'category': data["category"], 'name': data["name"],
                        'email': data["email"]}), 201

    else:
        return jsonify({'message': 'User already registered!'}), 403


@app.route("/api/login", methods=[POST])
@cross_origin()
def login():
    try:
        data = request.get_json()
        collection: pymongo.collection.Collection = db.auth
        registered = utils.signed_up(email=data['email'].lower())
        if not registered:
            return jsonify({'message': 'User Not registered!'}), 403
        elif utils.check_login(data['email'], data['password']):
            return jsonify({'message': 'Login Successful!', 'ID': data['ID']}), 200
    except Exception as e:
        return jsonify({'message': 'Error 500'}), 500


@app.route("/api/investorInfo", methods=[POST])
@cross_origin()
def investorInfo():
    try:
        data = request.get_json()
        collection: pymongo.collection.Collection = db.investors
        final = {'ID': db.auth.count(), 'preferences': data['preferences'], 'subPreferences': data['subPreferences'],
                 'investmentType': data['investmentType'], 'country': data['country'],
                 'description': data['description'], 'pastInvestments': data['pastInvestments'],
                 'validation': data['validation']}
        collection.insert_one(final)
        return jsonify({'message': 'Investors Info Registered!', 'ID': data['ID']}), 201
    except Exception as e:
        return jsonify({'message': 'Error 500'}), 500


@app.route("/api/projectInfo", methods=[POST])
@cross_origin()
def projectInfo():
    try:
        data = request.get_json()
        collection: pymongo.collection.Collection = db.projects
        final = {'ID': db.auth.count(), 'project': data['project'], 'intro': data['intro'],
                 'teamSize': data['teamSize'], 'category': data['category'], 'subCategory': data['subCategory'],
                 'description': data['description'], 'bestAchievements': data['bestAchievements'],
                 'links': data['links'], 'funding': data['expectedFunding'], 'pitch': data['pitch'],
                 'expectedROI': data['expectedROI'], 'country': data['country']}
        collection.insert_one(final)
        return jsonify({'message': 'Project Info Registered!', 'ID': data['ID']}), 201
    except Exception as e:
        return jsonify({'message': 'Error 500'}), 500


@app.route("/api/fetchAllProject", methods=[POST])
def fetchAllProject():
    data = request.get_json()
    try:
        conversion.mongoToCSV('investors', 'api/investors.csv')
        conversion.mongoToCSV('projects', 'api/projects.csv')
        similarity_array: list[float] = model.similarities(data['ID'])
        similarity_array.sort()

        return jsonify({})

    except Exception as e:
        print(e)
