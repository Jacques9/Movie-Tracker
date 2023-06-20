from fastapi import APIRouter, HTTPException, Depends
from api.models.movies import MovieReq, Movies

router = APIRouter(
    prefix='/movie'
)

movies = Movies()

@router.get('/all')
def get_all_movies():
    return movies.fetch_all_movies()
   