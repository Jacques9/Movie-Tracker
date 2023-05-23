from config import DB_NAME, CON_STR
from fastapi import FastAPI, HTTPException, Query
from pymongo.collection import Collection
from pydantic import BaseModel, Field
from bson.objectid import ObjectId
class UsersReq(BaseModel):
    username: str
    password: str
    email: str

class LoginReq(BaseModel):
    email: str
    password: str

class MovieReq(BaseModel):
    id: int

class UserReq(BaseModel):
    id: str = Field(..., alias='_id')

class Users:
    def __init__(self, collection: Collection) -> None:
        self.collection = collection
    
    def create_user(self, user_data: dict):
        self.collection.insert_one(user_data)

    def check_user_exists(self, email: str):
        return self.collection.find_one({'email': email})
    
    def get_all_users(self):
        return self.collection.find()
    
    def get_user(self, id: str):
        return self.collection.find_one({'_id': ObjectId(id)})
    
    def delete_user(self, id: str):
        result = self.collection.delete_one({'_id': ObjectId(id)})
        return result.deleted_count > 0
    
    def update(self, id: str, field: str, val: str):
        update_query = {
            '$set' : {field: val}
        }

        update_res = self.collection.update_one(
            {'_id': ObjectId(id)},
            update_query
        )

        return update_res.modified_count


class Movies:
    def __init__(self, collection: Collection) -> None:
        self.collection = collection
    
    def get_movie(self, id: int):
        return self.collection.find_one({'id': id})

    def get_all_movies(self):
        return self.collection.find()

    def delete_movie(self, id: int):
        result = self.collection.delete_one({'id': id})
        return result.deleted_count > 0
    
app = FastAPI()

from db_connect import users_collection, movies_collection

users_collection = Users(users_collection)
movies_collection = Movies(movies_collection)

@app.post('/user/register')
def register(user: UsersReq):
    def hash_password(password):
        import bcrypt
        salt = bcrypt.gensalt()

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

        return hashed_password.decode('utf-8')

    if users_collection.check_user_exists(user.email):
        raise HTTPException(status_code=400, detail='User already exists')

    from datetime import datetime
    user_data = {
        'username': user.username,
        'password': hash_password(user.password),
        'email': user.email,
        'created_at': datetime.today(),
        'type' : 'user',
        'favourites' : [] # array of objectid's
    }

    try:
        users_collection.create_user(user_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail='User registration failed')

    return {'message': 'User created'}

@app.post('/user/login')
def login(user: LoginReq):
    if (db_user := users_collection.check_user_exists(user.email)) is None:
        raise HTTPException(status_code=404, detail='User does not exist')
    
    import bcrypt
    hashed_password = db_user['password']
    if not bcrypt.checkpw(user.password.encode('utf-8'), hashed_password.encode('utf-8')):
        raise HTTPException(status_code=401, detail='Invalid password')
    
    return {'message': 'Login succesful'}


@app.get('/movie/find/{id}')
def get_movie(id: int):
    result = movies_collection.get_movie(id)

    if result is None:
        raise HTTPException(status_code=404, detail='Movie not found')

    return {
        'title': result['title'],
        'release_date': result['release_date'],
        'popularity': result['popularity'],
        'poster_path': result['poster_path'],
        'backdrop_path': result['backdrop_path'],
        'genre_names': result['genre_names']
    }

@app.get('/movies/all')
def get_all_movies():
    movies = movies_collection.get_all_movies()
    movies = list(movies)

    movies = list(
        map(
            lambda movie: {
                k: v for k, v in movie.items() if k!= '_id'
            }, movies
        )
    )
         
    return movies

@app.get('/users/all')
def get_all_users():
    users = users_collection.get_all_users()
    users = list(users)
    
    if len(users) == 0:
        raise HTTPException(status_code=404, detail='There are no users in DB')

    users = [{
        field: str(user[field]) if field == '_id' else user[field] for field in ['_id', 'username', 'email', 'password', 'type', 'created_at']
    } 
    for user in users]

    return users

@app.get('/users/find/{id}')
def get_user(id: str):
    result = users_collection.get_user(id)
    
    if result is None:
        raise HTTPException(status_code=404, detail='User not found')


    return {
        '_id': str(result['_id']),
        'username': result['username'],
        'email': result['email'],
        'created_at': result['created_at'],
        'type': result['type']
    }

@app.delete('/users/delete/{id}')
def del_user(id: str):
    if users_collection.delete_user(id):
        return {'message': 'User deleted succesfully'}
    else:
        raise HTTPException(status_code=404, detail='User not found')
    
@app.delete('/movie/delete/{id}')
def del_movie(id: int):
    if movies_collection.delete_movie(id):
        return {'message' : 'Movie deleted succesfully'}
    else:
        raise HTTPException(status_code=404, detail='Movie not found')
    
@app.put('/users/email/{id}') # url /users/email/{id}?email={new_email}
def replace_email(id: str, email: str):
    if not users_collection.get_user(id):
        raise HTTPException(status_code=404, detail='User not found')

    users_collection.update(id, 'email', email)

    return {
        'message': 'Email updated succesfully'
    }

@app.put('/users/username/{id}') # url /users/username/{id}?usr={new_username}
def replace_usr(id: str, usr: str):
    if not users_collection.get_user(id):
        raise HTTPException(status_code=404, detail='User not found')
    
    users_collection.update(id, 'username', usr)

    return {
        'message': 'Username updated succesfully'
    }

@app.put('/users/password/{id}') # url /users/username/{id}?pw={new_password}
def replace_pass(id: str, pw: str):
    def hash_password(password):
        import bcrypt
        salt = bcrypt.gensalt()

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

        return hashed_password.decode('utf-8')
    
    if not users_collection.get_user(id):
        raise HTTPException(status_code=404, detail='User not found')
    
    hashed_pass = hash_password(pw)

    users_collection.update(id, 'password', hashed_pass)

    return {
        'message': 'Password updated succesfully'
    }