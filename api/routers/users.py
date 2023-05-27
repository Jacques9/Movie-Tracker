from fastapi import APIRouter, HTTPException
from ..models.users import Users, UsersReq
from ..db_connect import users_collection

router = APIRouter(
    prefix='/user'
)

users_collection = Users(users_collection)

@router.post('/register') # url /user/register
def register(user: UsersReq):
    def hash_password(password):
        import bcrypt
        salt = bcrypt.gensalt()

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

        return hashed_password.decode('utf-8')

    if users_collection.check_user_exists(user.email):
        raise HTTPException(
            status_code=400, 
            detail='User already exists'
        )

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
        raise HTTPException(
            status_code=500, 
            detail='User registration failed'
        )

    return {
        'message': 'User created'
    }

@router.get('/all') # url /user/all
def get_all_users():
    users = users_collection.get_all_users()
    users = list(users)

    if len(users) == 0:
        raise HTTPException(
            status_code=404,
            detail='There are no users in DB'
        )
    
    users = [
        {
            field: str(user[field]) if field == '_id' else user[field] 
            for field in ['_id', 'username', 'email', 'type', 'created_at']
        } 
        for user in users
    ]

    return users

@router.get('/find/{id}') # url /user/find/{id}
def get_user(id: str):
    result = users_collection.get_user(id)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail='User not found'
        )
    
    return {
        '_id': str(result['_id']),
        'username': result['username'],
        'email': result['email'],
        'created_at': result['created_at'],
        'type': result['type']
    }

@router.delete('/delete/{id}') # url /user/delete/{id}
def delete_user(id: str):
    if users_collection.delete_user(id):
        return {
            'message': 'User deleted succesfully!'
        }
    else:
        raise HTTPException(
            status_code=404,
            detail='User not found'
        )