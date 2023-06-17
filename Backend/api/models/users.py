from pydantic import BaseModel, Field
from firebase_admin import auth
from db.connect import init_firestore

class UsersReq(BaseModel):
    username: str
    password: str
    email: str

class LoginReq(BaseModel):
    email: str
    password: str

class UserReq(BaseModel):
    id: str = Field(..., alias='_id')

class Users:
    def __init__(self) -> None:
        self.db = init_firestore()
        
    def check_if_exists(self, email: str) -> bool:
        try:
            auth.get_user_by_email(email)
            return True
        except auth.UserNotFoundError:
            return False
    
    def create_user(self, user: UsersReq) -> bool:   
        try:
            auth.create_user(
                email=user.email,
                password=user.password,
                display_name=user.username
            )
            

            from datetime import datetime

            user_data = {
                    'username': user.username,
                    'email': user.email,
                    'created_at': datetime.now().isoformat(),
                    'type': 'user',
                    'favorites': []
            }

            self.db.collection('users').add(user_data)        
        except Exception as _:
            return False

        return True
    
    def fetch_all_users(self):
        return self.db.collection('users').get()
    
    def fetch_a_user(self, id: str):
        return self.db.collection('users').document(id).get()

    def delete_a_user(self, user_data: str, id: str):
        try: 
            user = auth.get_user_by_email(user_data['email'])
            auth.delete_user(user.uid)
        except auth.UserNotFoundError as _:
            pass
        
        self.db.collection('users').document(id).delete()