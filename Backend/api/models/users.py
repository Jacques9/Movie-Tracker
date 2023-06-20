from pydantic import BaseModel, Field
from firebase_admin import auth
from db.connect import init_firestore
from fastapi import HTTPException
# from config import API_KEY
import requests

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
    
    # def authentificate(self, user: LoginReq):
    #     try:
    #         url = f'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}'

    #         payload = {
    #             'email': user.email,
    #             'password': user.password,
    #             'returnSecureToken': True
    #         }

    #         response = requests.post(
    #             url, json=payload
    #         )
    #         return response
    #         if response:
    #             return {'message': 'Login succesful'}
    #         else:
    #             raise HTTPException(
    #                 status_code=401,
    #                 detail='Invalid email or password'
    #             )
    #     except Exception as _:
    #         raise _

    def fetch_all_users(self):
        return self.db.collection('users').get()
    
    def fetch_a_user(self, id: str):
        return self.db.collection('users').document(id).get()

    def get_field_by(self, id: str, field: str):
        user_doc = self.db.collection('users').document(id).get()

        return user_doc.get(field)


    def update_username(self, id: str, new_usr: str):
        self.db.collection('users').document(id).update({
            'username': new_usr
        })

        email = self.get_field_by(id, 'email')

        user = auth.get_user_by_email(email)

        auth.update_user(
            user.uid,
            display_name=new_usr
        )

    def update_password(self, email: str, new_pass: str):
        try:
            user = auth.get_user_by_email(email)
            auth.update_user(
                user.uid,
                password=new_pass
            )
        except Exception:
            raise HTTPException(
                status_code=500,
                detail='Failed to update password'
            )

    def delete_a_user(self, user_data: str, id: str):
        try: 
            user = auth.get_user_by_email(user_data['email'])
            auth.delete_user(user.uid)
        except auth.UserNotFoundError as _:
            pass
        
        self.db.collection('users').document(id).delete()