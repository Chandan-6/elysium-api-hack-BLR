import os
import csv
import json
import pandas as pd

import pymongo.collection
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()

# Authenticating Mongo.
URI = f"mongodb+srv://{os.environ.get('USERNAME')}:{os.environ.get('PASSWORD')}@cluster0.qv3wn6u.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Creating the client variable.
client = MongoClient(URI, server_api=ServerApi('1'))


def csvToMongo(csvFileName: str, collectionName: str, headers=None) -> None:
    """
    Pushes a CSV file to the MongoDB collection "Data"
    :param csvFileName: The path of the CSV file to be copied
    :param collectionName: The name of the collection that will contain the data
    :param headers: The headers of the CSV file
    :return: None
    """
    try:
        csvFile = open(f"../assets/{csvFileName}.csv", 'r')
        reader = csv.DictReader(csvFile)
        collection = client["Data"][collectionName]
        for row in reader:
            temp = {}
            for field in headers:
                temp[field] = row[field]

            collection.insert_one(temp)
        print(f"Pushed the file {csvFile.name} to {collectionName}.")
    except Exception as e:
        print(f"Error: {e}")


def mongoToCSV(collection_name, csv_file_path):
    """
    Reads data from a MongoDB collection and stores it in a CSV file.

    Args:
        collection_name: The name of the collection to export.
        csv_file_path: The path to the CSV file to create.
    """

    try:
        # Connect to MongoDB
        db = client['Data']
        collection = db[collection_name]

        # Fetch data from MongoDB
        data = list(collection.find())

        # Convert MongoDB data to DataFrame
        df = pd.DataFrame(data)

        # Write DataFrame to CSV file
        df.to_csv(csv_file_path, index=False)

        print(f"Successfully exported data from '{collection_name}' to CSV file: '{csv_file_path}'")

    except Exception as e:
        print(f"Error: {e}")
