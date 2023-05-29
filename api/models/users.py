from pydantic import BaseModel, Field
from pymongo.collection import Collection
from bson.objectid import ObjectId

class Users:
    def __init__(self, collection: Collection) -> None:
        self.collection = collection
    
    def get_all_users(self):
        return self.collection.find()

    def check_user_exists(self, email: str):
        return self.collection.find_one({'email': email})

    def create_user(self, user_data: dict):
        self.collection.insert_one(user_data)
    
    def get_user(self, id: str):
        return self.collection.find_one(
            {'_id': ObjectId(id)}
        )
    
    def delete_user(self, id: str):
        result = self.collection.delete_one(
            {'_id': ObjectId(id)}
        )

        return result.deleted_count > 0

    def update(self, id: str, field: str, val: str):
        update_query = {
            '$set' : {
                field: val
            }
        }

        update_res = self.collection.update_one(
            {'_id': ObjectId(id)}, update_query
        )

        return update_res.modified_count
    
    def delete_favorite(self, user_id: str, movie_id: str):
        result = self.collection.update_one(
            {
                '_id': ObjectId(user_id)
            },
            {
                '$pull': {
                'favourites': ObjectId(movie_id)
                }
            }
        )

        return result.modified_count > 0

class UsersReq(BaseModel):
    username: str
    password: str
    email: str

class LoginReq(BaseModel):
    email: str
    password: str

class UserReq(BaseModel):
    id: str = Field(..., alias='_id')