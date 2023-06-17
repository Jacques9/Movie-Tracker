from fastapi import APIRouter, HTTPException, Query
from api.models.users import Users, UsersReq
from firebase_admin import auth

router = APIRouter (
    prefix='/user'
)

users = Users()

@router.post('/register') 
def register(user: UsersReq):
    if users.check_if_exists(user.email):
        raise HTTPException(
            status_code=400,
            detail='User already exists'
        )
    
    try:
        users.create_user(user)
    except Exception as _:
        raise HTTPException(
            status_code=500,
            detail='User registration failed'
        )

    return {
        'message': 'User created'
    }

@router.get('/all')
def get_all_users():
    all_users = users.fetch_all_users()

    if len(all_users) == 0:
        raise HTTPException(
            status_code=404,
            detail='There are no users in DB'
        )
    
    users_data = [
        {
            'id': user.id,
            'username': user.get('username'),
            'email': user.get('email'),
            'type': user.get('type'),
            'created_at': user.get('created_at'),
        }
        for user in all_users
    ]

    return users_data