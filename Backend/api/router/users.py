from fastapi import APIRouter, HTTPException, Query
from db.connect import users_collection
from api.models.users import Users, UserReq

router = APIRouter (
    prefix='/user'
)

users_collection = Users(users_collection)

@router.post('/register') 
def register(user: UserReq):
    if users_collection.check_if_exists(user.email):
        raise HTTPException(
            status_code=400,
            detail='User already exists'
        )
    
    