import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('movie-tracker-7ab60-firebase-adminsdk-y16h6-fac369a8a5.json')
firebase_admin.initialize_app(cred)

app = firebase_admin.get_app()

def get_firestore_client():
    db = firebase_admin.firestore.client(app)
    return db