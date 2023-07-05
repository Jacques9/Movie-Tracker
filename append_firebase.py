import firebase_admin, json, threading
from firebase_admin import credentials
from firebase_admin import firestore

def add_movie(collection_ref, movie):
    collection_ref.add(movie)

def load_db_from_json():
    # inlocuiește cu path-ul tau
    cred = credentials.Certificate('/home/norby/Coding/Projectz/MovieTracker/movie-tracker-7ab60-firebase-adminsdk-y16h6-fac369a8a5.json')
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

def edit_movies():
    cred = credentials.Certificate('movie-tracker-7ab60-firebase-adminsdk-y16h6-fac369a8a5.json')
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    
    collection_ref = db.collection('movies')

    movies = collection_ref.get()

    for movie in movies:
        movie_dict = movie.to_dict()
        movie_dict['reviews'] = []
        movie.reference.set(movie_dict)


load_db_from_json()