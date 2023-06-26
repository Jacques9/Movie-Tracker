from fastapi import APIRouter, HTTPException, Depends
from api.models.movies import MovieReq, Movies

router = APIRouter(
    prefix='/movie'
)

movies = Movies()

@router.get('/all')
def get_all_movies():
    return movies.fetch_all_movies()

@router.get('/{id}')
def get_movie_by_id(id: str):
    return movies.fetch_movie_by_id(id)

@router.delete('/{id}')
def remove_movie_by_id(id: str):
    return movies.delete_movie_by_id(id)