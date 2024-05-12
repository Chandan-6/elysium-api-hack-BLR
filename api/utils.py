import os
import csv
import json
import pandas as pd
import time

import encryption.encryption as encryption
from mongo import conversion

import pymongo.collection
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()

# Authenticating Mongo.
URI = f"mongodb+srv://{os.environ.get('USERNAME')}:{os.environ.get('PASSWORD')}@cluster0.qv3wn6u.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Creating the client variable.
client = MongoClient(URI, server_api=ServerApi('1'))
db = client['Data']

investors = db['investors']
projects = db['projects']
auth = db['auth']


def signed_up(name: str = None, email: str = None, category: str = None) -> bool:
    name = name is not None and auth.find_one({'Name': name.lower()}) is not None and True or False
    email = email is not None and auth.find_one({'Email': email.lower()}) is not None and True or False
    category = category is not None and name is not None and auth.find_one({'Category': category.lower()}) is not None and True or False

    return ((name and category) or (email and category)) and not(email and name and category)


def check_login(email: str, password: str) -> bool:
    for iteration in auth.find():
        if iteration['Email'] == email and iteration['Password'] == encryption.sha256_encrypt(password):
            return True

    return False
