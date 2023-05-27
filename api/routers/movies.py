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