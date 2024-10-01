from pydantic import BaseModel
from pymongo.collection import Collection

class blogDocument(BaseModel):
    blog_id:str
    blog_owner_id:str
    blog_title:str
    blog_text:str
    blog_created_at:float
    blog_updated_at:float

class userDocument(BaseModel):
    user_id:str
    username:str
    name:str
    lastname:str
    email:str
    password:str
    user_created_at:float
    user_updated_at:float

class commentDocument(BaseModel):
    comment_id:str
    comment_blog_id:str
    comment_owner_id:str
    comment_text:str
    comment_created_at:float
    comment_updated_at:float

class mongoDocs(BaseModel):
    class Config:
        arbitrary_types_allowed = True
    users: Collection
    blogs: Collection
    comments: Collection

class UserInDB(userDocument):
    password: str

class TokenData(BaseModel):
    username: str | None = None

