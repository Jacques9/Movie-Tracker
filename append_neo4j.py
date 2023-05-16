import json
from config import CON_STR_NEO4J, PASS
from neo4j import GraphDatabase

def add_movie(tx, movie):
    query = (
        "MERGE (m:Movie {id: $id}) "
        "SET m.title = $title, "
        "m.original_title = $original_title, "
        "m.release_date = $release_date, "
        "m.popularity = $popularity, "
        "m.vote_average = $vote_average, "
        "m.vote_count = $vote_count, "
        "m.overview = $overview, "
        "m.poster_path = $poster_path, "
        "m.backdrop_path = $backdrop_path, "
        "m.original_language = $original_language, "
        "m.adult = $adult, "
        "m.video = $video, "
        "m.genre_names = $genre_names"
    )
    tx.run(query, **movie)


with open('Movie-Tracker/movies.json') as f:
        movies = json.load(f)

driver = GraphDatabase.driver(CON_STR_NEO4J, auth=('neo4j', PASS))

with driver.session() as session:
    for movie in movies:
        session.execute_write(add_movie, movie)
        break