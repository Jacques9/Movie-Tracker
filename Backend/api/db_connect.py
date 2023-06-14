from config import DB_NAME, CON_STR
from pymongo import MongoClient

client = MongoClient(CON_STR)
db = client[DB_NAME]

users_collection = db['users']
movies_collection = db['movies']
