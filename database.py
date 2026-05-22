from flask_pymongo import PyMongo
from pymongo import MongoClient

mongo = PyMongo()

def get_db():
    return mongo.db
