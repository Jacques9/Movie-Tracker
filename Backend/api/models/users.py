from pydantic import BaseModel, Field
from firebase_admin import auth

class Users:
    def __init__(self, collection) -> None:
        self.collection = collection

    def check_if_exists(self, email: str) -> bool:
        try:
            auth.get_user_by_email(email)
            return True
        except auth.UserNotFoundError:
            return False

class UsersReq(BaseModel):
    username: str
    password: str
    email: str

class LoginReq(BaseModel):
    email: str
    password: str

class UserReq(BaseModel):
    id: str = Field(..., alias='_id')