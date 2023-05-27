from fastapi import APIRouter, HTTPException
from ..models.movies import MovieReq, Movies
from ..db_connect import movies_collection

router = APIRouter(
    prefix='/movie'
)

movies_collection = Movies(movies_collection)

@router.get('/all')
def get_all_movies():
    movies = movies_collection.get_all_movies()
    movies = list(movies)

    movies = list(
        map(
            lambda movie: {
                k: v for k, v in movie.items() if k!='_id'
            }, movies
        )
    )

    return movies

@router.get('/find/{id}')
def get_movie(id: str):
    result = movies_collection.get_movie(id)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail='Movie not found'
        )
    
    return {
        '_id': str(result['_id']),
        'title': result['title'],
        'release_date': result['release_date'],
        'popularity': result['popularity'],
        'poster_path': result['poster_path'],
        'backdrop_path': result['backdrop_path'],
        'genre_names': result['genre_names']
    }

@router.delete('/delete/{id}')
def delete_movie(id: str):
    if movies_collection.delete_movie(id):
        return {
            'message': 'Movie deleted succesfully!'
        }
    else: 
        raise HTTPException(
            status_code=404,
            detail='Movie not found'
        )