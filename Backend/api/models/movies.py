from pydantic import BaseModel, Field
from firebase_admin import auth
from db.connect import get_firestore_client
from fastapi import HTTPException
import firebase_admin

class MovieReq(BaseModel):
    id: str = Field(..., alias='_id')


class Movies:
    def __init__(self) -> None:
        self.db = get_firestore_client()

    def fetch_all_movies(self):
        # reminder to change limit
        # maybe maybe lru caching the movies later
        movies_ref = self.db.collection('movies').limit(50) 
        all_movies = [doc.to_dict() for doc in movies_ref.stream()]
        return all_movies
    