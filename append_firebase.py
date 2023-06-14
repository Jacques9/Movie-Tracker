import json, pymongo
from config import DB_NAME, CON_STR

def load_db_from_json():
    import threading
    with open('movies.json') as f:
        movies = json.load(f)

    client = pymongo.MongoClient(CON_STR)

    db = client[DB_NAME]

    if 'movies' not in db.list_collection_names():
        db.create_collection('movies')
    
    threads = []
    for movie in movies:
        thread = threading.Thread(target=db.movies.insert_one, args=(movie,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
    

load_db_from_json()