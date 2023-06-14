from config import DB_NAME, CON_STR
from pymongo.collection import Collection
from pydantic import BaseModel, Field
from bson.objectid import ObjectId

class MovieReq(BaseModel):
    id: str = Field(..., alias='_id')

class Movies:
    def __init__(self, collection: Collection) -> None:
        self.collection = collection
    
    def get_movie(self, id: str):
        return self.collection.find_one({'_id': ObjectId(id)})

    def get_all_movies(self):
        return self.collection.find()

    def delete_movie(self, id: int):
        result = self.collection.delete_one({'_id': ObjectId(id)})
        return result.deleted_count > 0