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
        
        user_ref = self.db.collection('users').document(user_id)
        user_data = user_ref.get().to_dict()

        if not user_data:
            return {'message': 'User not found.'}

        username = user_data.get('username', '')

        review = {
            'user_id': user_id,
            'text': text,
            'username': username,
            'stars': stars
        }

        movie_data = self.fetch_movie_by_id(movie_id)
        if 'reviews' not in movie_data:
            movie_data['reviews'] = []

        movie_ref = self.db.collection('movies').document(movie_id)
        review_doc_ref = movie_ref.collection('reviews').document()
        review_id = review_doc_ref.id

        movie_data['reviews'] = [review_data for review_data in movie_data['reviews'] if review_data['review_id'] != review_id]
        movie_data['reviews'].append({
            'review_id': review_id,
            'review_data': review
        })

        movie_ref.set(movie_data, merge=True)

        if 'user_reviews' not in user_data:
            user_data['user_reviews'] = []

        user_data['user_reviews'].append(review_doc_ref)

        user_ref.set(user_data, merge=True)

        return {'message': 'Review added successfully.'}
        
    def get_movie_reviews(self, movie_id: str):
        movie_ref = self.db.collection('movies').document(movie_id)
        movie_doc = movie_ref.get()

        if movie_doc.exists:
            movie_data = movie_doc.to_dict()
            reviews = [review['review_data'] for review in movie_data.get('reviews', [])]
            return reviews
        else:
            raise HTTPException(status_code=404, detail='Movie not found')
        
    def delete_movie_review(self, user_id: str, movie_id: str):
        movie_ref = self.db.collection('movies').document(movie_id)
        movie_doc = movie_ref.get()

        if movie_doc.exists:
            movie_data = movie_doc.to_dict()
            reviews = movie_data.get('reviews', [])

            review_id = None
            for review in reviews:
                if review['review_data']['user_id'] == user_id:
                    review_id = review['review_id']
                    break

            if review_id:
                reviews = [review for review in reviews if review['review_id'] != review_id]
                movie_data['reviews'] = reviews
                movie_ref.set(movie_data, merge=True)
                
                user_ref = self.db.collection('users').document(user_id)
                user_data = user_ref.get().to_dict()
                user_reviews = user_data.get('user_reviews', [])
                user_reviews = [review_ref for review_ref in user_reviews if review_ref.id != review_id]
                user_data['user_reviews'] = user_reviews
                user_ref.set(user_data, merge=True)

                return {'message': 'Review deleted successfully.'}
            else:
                raise HTTPException(status_code=404, detail='Review not found for the given user and movie.')
        else:
            raise HTTPException(status_code=404, detail='Movie not found.')