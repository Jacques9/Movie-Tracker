from pydantic import BaseModel, Field

class Users:
    def __init__(self, collection) -> None:
        self.collection = collection

class UsersReq(BaseModel):
    username: str
    password: str
    email: str

class LoginReq(BaseModel):
    email: str
    password: str

class UserReq(BaseModel):
    id: str = Field(..., alias='_id')