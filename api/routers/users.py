from fastapi import APIRouter, HTTPException, Query
from ..models.users import Users, UsersReq
from ..db_connect import users_collection

def hash_password(password):
    import bcrypt
    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_password.decode('utf-8')

router = APIRouter(
    prefix='/user'
)

users_collection = Users(users_collection)

@router.post('/register') # url /user/register
def register(user: UsersReq):
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

@router.put('/username/{id}') # url /user/username/{id}
def replace_username(id: str, new_username: str):
    user = users_collection.get_user(id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail='User not found'
        )
    
    users_collection.update(id, 'username', new_username)

    return {
        'message': 'Username updated succesfully!'
    }

@router.put('/password/{id}') # url /user/password/{id}
def replace_password(id: str, new_password: str):
    if not users_collection.get_user(id):
        raise HTTPException(
            status_code=404, 
            detail='User not found'
        )
    
    hashed_pass = hash_password(new_password)

    users_collection.update(id, 'password', hashed_pass)

    return {
        'message': 'Password changed succesfully'
    }

@router.delete('/favorites')
def delete_fav(user_id: str = Query(..., description='User id')
               , movie_id: str = Query(..., description='Movie id')):
    if not users_collection.get_user(user_id):
        raise HTTPException(
            status_code=404, 
            detail='User not found'
        )
    
    res = users_collection.delete_favorite(
        user_id,
        movie_id
    )

    if res == 0:
        raise HTTPException(
            status_code=404, 
            detail='Oh no'
        )
    
    return {
        'message': 'Movie deleted succesfully from favorites!'
    }