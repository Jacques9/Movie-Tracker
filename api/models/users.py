from pydantic import BaseModel, Field
from pymongo.collection import Collection

class Users:
    def __init__(self, collection: Collection) -> None:
        self.collection = collection
    
    def get_all_users(self):
        return self.collection.find()

    def check_user_exists(self, email: str):
        return self.collection.find_one({'email': email})

    def create_user(self, user_data: dict):
        self.collection.insert_one(user_data)


class UsersReq(BaseModel):
    username: str
    password: str
    email: str

class LoginReq(BaseModel):
    email: str
    password: str

class UserReq(BaseModel):
    id: str = Field(..., alias='_id')