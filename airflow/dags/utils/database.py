import os
import json
from pymongo import MongoClient


def get_db_connection():
    conn_str = os.environ['DB_CONN']
    db_name = os.environ['DB_NAME']
    collection = os.environ['COLLECTION']
    client = MongoClient('{0}{1}'.format(conn_str, db_name))
    db = client[db_name]
    return db[collection]


def db_inser_file(file_name):
    with open(file_name) as jsonf:
        data = json.load(jsonf)
        db_insert_json(data)


def db_insert_json(json_data):
    db = get_db_connection()
    db.insert_many(json_data)
