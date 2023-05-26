from pydantic import BaseModel, Field
from pymongo.collection import Collection

class UsersReq(BaseModel):
    username: str
    password: str
    email: str

class LoginReq(BaseModel):
    email: str
    password: str

class MovieReq(BaseModel):
    id: int

class UserReq(BaseModel):
    id: str = Field(..., alias='_id')

class Users:
    def __init__(self, collection: Collection) -> None:
        self.collection = collection
        # self.SECRET_KEY = secrets.token_urlsafe(32)
    
    def create_user(self, user_data: dict):
        self.collection.insert_one(user_data)

    # def check_user_exists(self, email: str):
    #     return self.collection.find_one({'email': email})
    
    # def get_all_users(self):
    #     return self.collection.find()
    
    # def get_user(self, id: str):
    #     return self.collection.find_one({'_id': ObjectId(id)})
    
    # def delete_user(self, id: str):
    #     result = self.collection.delete_one({'_id': ObjectId(id)})
    #     return result.deleted_count > 0
    
    # def update(self, id: str, field: str, val: str):
    #     update_query = {
    #         '$set' : {field: val}
    #     }

    #     update_res = self.collection.update_one(
    #         {'_id': ObjectId(id)}, update_query
    #     )

    #     return update_res.modified_count
    
    # def generate_token(self, user_id: str, user_type):
    #     expires_delta = timedelta(minutes=30)
    #     expire = datetime.utcnow() + expires_delta

    #     payload = {
    #         "user_id": user_id, 
    #         "user_type": user_type,
    #         "exp": expire
    #     }
    #     token = jwt.encode(payload, self.SECRET_KEY, algorithm="HS256")

    #     return token   

    # def get_token_info(self, access_token: str):
    #     token_info = jwt.decode(access_token, verify=False, algorithms="HS256", key=self.SECRET_KEY)

    #     user_id = token_info.get("user_id")
    #     user_type = token_info.get("user_type")

    #     return user_id, user_type
    
    # def destroy_token(self, access_token: str):
    #     token_info = jwt.decode(access_token, verify=False, algorithms="HS256", key=self.SECRET_KEY)
    #     token_info['exp'] = datetime.utcnow() - timedelta(minutes=1)
    #     token = jwt.encode(token_info, self.SECRET_KEY, algorithm="HS256")
    #     return token.decode('utf-8')