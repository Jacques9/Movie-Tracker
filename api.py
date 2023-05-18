from config import DB_NAME, CON_STR
from fastapi import FastAPI
from pymongo.collection import Collection
from pydantic import BaseModel

class UsersReq(BaseModel):
    username: str
    password: str
    email: str

class LoginReq(BaseModel):
    email: str
    password: str

class MovieReq(BaseModel):
    title: str

class Users:
    def __init__(self, collection: Collection) -> None:
        self.collection = collection
    
    def create_user(self, user_data: dict):
        self.collection.insert_one(user_data)

    def check_user_exists(self, email: str):
        return self.collection.find_one({'email': email})

class Movies:
    def __init__(self, collection: Collection) -> None:
        self.collection = collection
    
    def find_movie(self, title: str):
        return self.collection.find_one({'title': title})

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
        return {'message': 'user already exists'}

    user_data = {
        'username': user.username,
        'password': hash_password(user.password),
        'email': user.email,
        'favourites' : [] # array of objectid's
    }

    users_collection.create_user(user_data)

    return {'message': 'user created'}

@app.post('/user/login')
def login(user: LoginReq):
    if (db_user := users_collection.check_user_exists(user.email)) is None:
        return {'message': 'User does not exist'}
    
    import bcrypt
    hashed_password = db_user['password']
    if not bcrypt.checkpw(user.password.encode('utf-8'), hashed_password.encode('utf-8')):
        return {'message': 'Invalid password'}
    
    return {'message': 'Login succesful'}

@app.get('/movie/find')
def get_movie(movie: MovieReq):
    result = movies_collection.find_movie(movie.title)

    if result is None:
        return {'message': 'Invalid password'}
    
    return result