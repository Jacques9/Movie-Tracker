import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

def init_firestore():
    # add json path
    cred = credentials.Certificate('/home/norby/Coding/Projectz/MovieTracker/movie-tracker-7ab60-firebase-adminsdk-y16h6-fac369a8a5.json')
    firebase_admin.initialize_app(cred)

    db = firestore.client()

    return db

def create_collection(db, collection_name):
    collection_ref = db.collection(collection_name)

    return collection_ref

db = init_firestore()

users_collection = create_collection(db, 'users')
movies_collection = create_collection(db, 'movies')