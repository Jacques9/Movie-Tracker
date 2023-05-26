import requests, time, json
from config import API_KEY

def setup():
    BASE_URL = 'https://api.themoviedb.org/3'
    DISCOVER_URL = f'{BASE_URL}/discover/movie'
    GENRE_URL = f'{BASE_URL}/genre/movie/list'

    params = {
        'api_key': API_KEY,
        'sort_by': 'popularity.desc',
        'page': 1,
        'vote_count.gte': 1000,
        'language': 'en-US'
    }

    genre_response = requests.get(GENRE_URL, params={'api_key': API_KEY})
    genre_data = genre_response.json().get('genres')
    genre_map = {genre['id']: genre['name'] for genre in genre_data}

    return (
        BASE_URL,
        DISCOVER_URL,
        GENRE_URL,
        params,
        genre_map
    )

def get_movies():
    BASE_URL, DISCOVER_URL, GENRE_URL, params, genre_map = setup()
    movies = []

    for i in range(1, 340):
        params['page'] = i
        response = requests.get(DISCOVER_URL, params=params)
        results = response.json().get('results')
        
        for result in results:
            genre_names = [genre_map.get(genre_id) for genre_id in result['genre_ids']]
            movie_data = {
                'title': result['title'],
                'original_title': result['original_title'],
                'release_date': result['release_date'],
                'popularity': result['popularity'],
                'vote_average': result['vote_average'],
                'vote_count': result['vote_count'],
                'overview': result['overview'],
                'poster_path': result['poster_path'],
                'backdrop_path': result['backdrop_path'],
                'original_language': result['original_language'],
                'adult': result['adult'],
                'video': result['video'],
                'genre_names': genre_names, 
            }
            movies.append(movie_data)

        if i % 40 == 0:
            time.sleep(10)

    with open('movies.json', 'a') as f:
        json.dump(movies, f, indent=4)

if __name__ == '__main__':
    get_movies()