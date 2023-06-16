import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

def init_firestore():
    # add json path
    cred = credentials.Certificate('/home/norby/Coding/Projectz/MovieTracker/movie-tracker-7ab60-firebase-adminsdk-y16h6-fac369a8a5.json')
    firebase_admin.initialize_app(cred)

    db = firestore.client()

    return db
