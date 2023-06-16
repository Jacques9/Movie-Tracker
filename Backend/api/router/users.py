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
    

    hashed_pass = auth.create_user(
        email=user.email,
        password=user.password,
        display_name=user.username
    ).uid

    try:
        users.create_user(user, hashed_pass)
    except Exception as _:
        raise HTTPException(
            status_code=500,
            detail='User registration failed'
        )

    return {
        'message': 'User created'
    }