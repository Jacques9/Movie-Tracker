from pydantic import BaseModel, Field
from firebase_admin import auth
from db.connect import get_firestore_client
from fastapi import HTTPException
from config import API_KEY
import requests

class UsersReq(BaseModel):
    username: str
    password: str
    email: str

class LoginReq(BaseModel):
    email: str
    password: str

class UserReq(BaseModel):
    id: str = Field(..., alias='_id')

class Users:
    def __init__(self) -> None:
        self.db = get_firestore_client()
        
    def check_if_exists(self, email: str) -> bool:
        try:
            auth.get_user_by_email(email)
            return True
        except auth.UserNotFoundError:
            return False
    
    def create_user(self, user: UsersReq) -> bool:   
        try:
            auth.create_user(
                email=user.email,
                password=user.password,
                display_name=user.username
            )
            

            from datetime import datetime

            user_data = {
                    'username': user.username,
                    'email': user.email,
                    'created_at': datetime.now().isoformat(),
                    'type': 'user',
                    'profile_pic': '',
                    'user_reviews': [],
                    'favorites': [],
                    'watched': [],
                    'watching': []
            }

            self.db.collection('users').add(user_data)        
        except Exception as _:
            return False

        return True
    
    def authentificate(self, user: LoginReq):
        try:
            url = f'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}'

            payload = {
                'email': user.email,
                'password': user.password,
                'returnSecureToken': True
            }

            response = requests.post(url, json=payload)
            response = response.json()

            if 'idToken' in response:
                uid = response['localId']
                
                users_collection = self.db.collection('users')
                user_query = users_collection.where('email', '==', user.email).limit(1)
                user_docs = user_query.get()

                if len(user_docs) > 0:
                    user_doc = user_docs[0]
                    user_id = user_doc.id
                    user_type = user_doc.get('type')


                    auth.set_custom_user_claims(
                        uid,
                        {
                            'userType': user_type
                        }
                    )

                    return {'message': 'Login successful', 'idToken': response['idToken'], 'user_id': user_id}
                else:
                    raise HTTPException(
                        status_code=404,
                        detail='User not found'
                    )
            else:
                raise HTTPException(
                    status_code=401,
                    detail='Invalid email or password'
                )
        except Exception as _:
            raise _

    def fetch_all_users(self):
        return self.db.collection('users').get()
    
    def fetch_a_user(self, id: str):
        return self.db.collection('users').document(id).get()

    def get_field_by(self, id: str, field: str):
        user_doc = self.db.collection('users').document(id).get()

        return user_doc.get(field)

    def fetch_a_user(self, field: str, value: str):
        users_ref = self.db.collection('users')
        
        query = users_ref.where('email', '==', value).limit(1)
        user_docs = query.get()

        if len(user_docs) > 0:
            user_doc = user_docs[0]
            return user_doc.get(field)
        else:
            return None
 
    def update_username(self, id: str, new_usr: str):
        self.db.collection('users').document(id).update({
            'username': new_usr
        })

        email = self.get_field_by(id, 'email')

        user = auth.get_user_by_email(email)

        auth.update_user(
            user.uid,
            display_name=new_usr
        )

    def update_password(self, email: str, new_pass: str):
        try:
            user = auth.get_user_by_email(email)
            auth.update_user(
                user.uid,
                password=new_pass
            )
        except Exception:
            raise HTTPException(
                status_code=500,
                detail='Failed to update password'
            )

    def delete_a_user(self, user_data: str, id: str):
        try: 
            user = auth.get_user_by_email(user_data['email'])
            auth.delete_user(user.uid)
        except auth.UserNotFoundError as _:
            pass
        
        self.db.collection('users').document(id).delete()

    def add_movie_to_favorites(self, user_id: str, movie_id: str):
        try:
            user_ref = self.db.collection('users').document(user_id)

            user_doc = user_ref.get()
            if not user_doc.exists:
                raise HTTPException(status_code=404, detail='User not found')

            user_data = user_doc.to_dict()
            favorites = user_data.get('favorites', [])

            if movie_id in favorites:
                raise HTTPException(status_code=400, detail='Movie already in favorites')

            favorites.append(movie_id)

            user_ref.update({'favorites': favorites})

            return {'message': 'Movie added to favorites'}
        
        except HTTPException:
            raise  
        except Exception as e:
            raise HTTPException(status_code=500, detail='Failed to add movie to favorites')
        
    def remove_movie_from_fav(self, user_id: str, movie_id: str):
        try:
            user_ref = self.db.collection('users').document(user_id)

            user_doc = user_ref.get()
            if not user_doc.exists:
                raise HTTPException(status_code=404, detail='User not found')

            user_data = user_doc.to_dict()
            favorites = user_data.get('favorites', [])

            if movie_id not in favorites:
                raise HTTPException(status_code=400, detail='Movie not found in favorites')

            favorites.remove(movie_id)

            user_ref.update({'favorites': favorites})

            return {'message': 'Movie removed from favorites'}
        except HTTPException:
            raise  
        except Exception as e:
            raise HTTPException(status_code=500, detail='Failed to remove movie from favorites')
        
    def add_to_watched(self, user_id: str, movie_id: str):
        try:
            user_ref = self.db.collection('users').document(user_id)

            user_doc = user_ref.get()
            if not user_doc.exists:
                raise HTTPException(status_code=404, detail='User not found')

            user_data = user_doc.to_dict()

            favorites = user_data.get('favorites', [])
            if movie_id in favorites:
                favorites.remove(movie_id)
                user_ref.update({'favorites': favorites})

            watched = user_data.get('watched', [])
            if movie_id not in watched:
                watched.append(movie_id)
                user_ref.update({'watched': watched})

            return {'message': 'Movie added to watched list'}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail='Failed to add movie to watched list')
        
    def delete_from_watched(self, user_id: str, movie_id: str):
        try:
            user_ref = self.db.collection('users').document(user_id)

            user_doc = user_ref.get()
            if not user_doc.exists:
                raise HTTPException(status_code=404, detail='User not found')

            user_data = user_doc.to_dict()

            watched = user_data.get('watched', [])
            if movie_id in watched:
                watched.remove(movie_id)
                user_ref.update({'watched': watched})

            return {'message': 'Movie removed from watched list'}
        except HTTPException:
            raise  
        except Exception as e:
            raise HTTPException(status_code=500, detail='Failed to remove movie from watched list')
        
    def add_to_watching(self, user_id: str, movie_id: str):
        try:
            user_ref = self.db.collection('users').document(user_id)

            user_doc = user_ref.get()
            if not user_doc.exists:
                raise HTTPException(status_code=404, detail='User not found')

            user_data = user_doc.to_dict()

            favorites = user_data.get('favorites', [])
            if movie_id in favorites:
                favorites.remove(movie_id)
                user_ref.update({'favorites': favorites})

            watched = user_data.get('watched', [])
            if movie_id in watched:
                raise HTTPException(status_code=400, detail='Movie already in watched list')

            watching = user_data.get('watching', [])
            if movie_id in watching:
                raise HTTPException(status_code=400, detail='Movie already in watching list')

            watching.append(movie_id)
            user_ref.update({'watching': watching})

            return {'message': 'Movie added to watching list'}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail='Failed to add movie to watching list')
        
    def remove_movie_from_watching(self, user_id: str, movie_id: str):
        try:
            user_ref = self.db.collection('users').document(user_id)

            user_doc = user_ref.get()
            if not user_doc.exists:
                raise HTTPException(status_code=404, detail='User not found')

            user_data = user_doc.to_dict()

            watching = user_data.get('watching', [])
            if movie_id in watching:
                watching.remove(movie_id)
                user_ref.update({'watching': watching})

            return {'message': 'Movie removed from watching list'}
        except HTTPException:
            raise  
        except Exception as e:
            raise HTTPException(status_code=500, detail='Failed to remove movie from watching list')
        
    def fetch_favorites_by_id(self, user_id: str):
        try:
            user_doc = self.db.collection('users').document(user_id).get()
            if not user_doc.exists:
                raise HTTPException(status_code=404, detail='User not found')

            user_data = user_doc.to_dict()
            favorites = user_data.get('favorites', [])

            movies = []
            for movie_id in favorites:
                movie = self.fetch_movie_by_id(movie_id)
                movies.append(movie)

            return movies
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail='Failed to fetch favorites')
    
    def fetch_watching_by_id(self, user_id: str):
        try:
            user_doc = self.db.collection('users').document(user_id).get()
            if not user_doc.exists:
                raise HTTPException(status_code=404, detail='User not found')

            user_data = user_doc.to_dict()
            watching = user_data.get('watching', [])

            movies = []
            for movie_id in watching:
                movie = self.fetch_movie_by_id(movie_id)
                movies.append(movie)

            return movies
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail='Failed to fetch watching list')
    
    def fetch_watched_by_id(self, user_id: str):
        try:
            user_doc = self.db.collection('users').document(user_id).get()
            if not user_doc.exists:
                raise HTTPException(status_code=404, detail='User not found')

            user_data = user_doc.to_dict()
            watched = user_data.get('watched', [])

            movies = []
            for movie_id in watched:
                movie = self.fetch_movie_by_id(movie_id)
                movies.append(movie)

            return movies
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail='Failed to fetch watched list')
    
    def fetch_movie_by_id(self, movie_id: str):
        try:
            movie_doc = self.db.collection('movies').document(movie_id).get()
            if movie_doc.exists:
                movie_data = movie_doc.to_dict()
                movie_data['id'] = movie_doc.id
                return movie_data
            else:
                raise HTTPException(status_code=404, detail='Movie not found')
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail='Failed to fetch movie')
        
    def fetch_user_reviews(self, user_id: str):
        user_ref = self.db.collection('users').document(user_id)
        user_data = user_ref.get().to_dict()
        user_reviews = user_data.get('user_reviews', [])

        review_data_list = []
        for review_ref in user_reviews:
            review_reference = review_ref.path

            split_parts = review_reference.split("/reviews/")
            movie_id = split_parts[0].split("/")[1]
            review_id = split_parts[1]

            movie_doc_ref = self.db.collection('movies').document(movie_id)
            movie_doc = movie_doc_ref.get()

            if movie_doc.exists:
                movie_data = movie_doc.to_dict()
                reviews = movie_data.get('reviews', [])

                for review in reviews:
                    if review.get('review_id') == review_id:
                        review_data = review.get('review_data')
                        review_data_list.append(review_data)
                        break

        return review_data_list