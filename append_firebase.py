import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
import threading

def add_movie(collection_ref, movie):
    collection_ref.add(movie)

def load_db_from_json():
    cred = credentials.Certificate('path/to/serviceAccountKey.json')
    firebase_admin.initialize_app(cred)

    db = firestore.client()

    with open('movies.json') as f:
        movies = json.load(f)

    collection_ref = db.collection('movies')

    threads = []
    for movie in movies:
        thread = threading.Thread(target=add_movie, args=(collection_ref, movie))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

load_db_from_json()