import firebase_admin, json, threading
from firebase_admin import credentials
from firebase_admin import firestore

def add_movie(collection_ref, movie):
    collection_ref.add(movie)

def load_db_from_json():
    # inlocuiește cu path-ul tau
    cred = credentials.Certificate('/home/norby/Coding/Projectz/Movie_Tracker/Movie-Tracker/movie-tracker-7ab60-firebase-adminsdk-y16h6-fac369a8a5.json')
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