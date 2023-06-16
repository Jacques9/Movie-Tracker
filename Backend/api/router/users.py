from fastapi import APIRouter, HTTPException, Query
from db.connect import users_collection
from api.models.users import Users, UserReq

router = APIRouter (
    prefix='/user'
)

users_collection = Users(users_collection)