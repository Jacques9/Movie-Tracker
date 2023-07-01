from pydantic import BaseModel, Field
from firebase_admin import auth, firestore
from db.connect import get_firestore_client
from fastapi import HTTPException
import firebase_admin

class MovieReq(BaseModel):
    id: str = Field(..., alias='_id')


class Movies:
    def __init__(self) -> None:
        self.db = get_firestore_client()

    def fetch_all_movies(self):
        movies_ref = self.db.collection('movies').limit(50)
        all_movies = []

        for doc in movies_ref.stream():
            movie_data = doc.to_dict()
            movie_data['id'] = doc.id
            all_movies.append(movie_data)
        return all_movies
    
    def fetch_movie_by_id(self, movie_id: str):
        movie_doc = self.db.collection('movies').document(movie_id).get()
        if movie_doc.exists:
            return movie_doc.to_dict()
        else:
            raise HTTPException(status_code=404, detail='Movie not found')
    
    def delete_movie_by_id(self, id: str):
        try:
            movie_ref = self.db.collection('movies').document(id)

            movie_doc = movie_ref.get()
            if not movie_doc.exists:
                raise HTTPException(status_code=404, detail='Movie not found')

            movie_ref.delete()

            return {'message': 'Movie deleted successfully'}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail='Failed to delete movie')
    
    def add_review(self, user_id: str, movie_id: str, text: str, stars: int):
        review = {
            'user_id': user_id,
            'text': text,
            'stars': stars
        }

        movie_data = self.fetch_movie_by_id(movie_id)
        if 'reviews' not in movie_data:
            movie_data['reviews'] = []

        movie_data['reviews'].append(review)

        movie_ref = self.db.collection('movies').document(movie_id)
        movie_ref.set(movie_data, merge=True)

        return {'message': 'Review added successfully.'}