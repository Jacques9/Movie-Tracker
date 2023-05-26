from fastapi import APIRouter, HTTPException
from ..schemas import UserReq, LoginReq, Users
from ..db_connect import users_collection

router = APIRouter(
    prefix='/user'
)

users_collection = Users(users_collection)

@router.post('/register')
def register(user: UserReq):
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

    return {
        'message': 'User created'
    }