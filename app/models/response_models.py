from pydantic import BaseModel
from typing import Optional, List

class createResponseModel(BaseModel):
    message:str

class deleteResponseModel(BaseModel):
    message:str

class updateResponseModel(BaseModel):
    message:str

class registerResponseModel(BaseModel):
    message:str

class getProfileDetailResponseModel(BaseModel):
    user_id:str
    username:str
    name:str
    lastname:str
    email:str
    user_created_at:float
    user_updated_at:float

class LoginToken(BaseModel):
    username:str
    access_token: str

#todo - this model will be deleted on the final
class Token(BaseModel):
    access_token: str
    token_type: str

class getBlogDetailResponseModel(BaseModel):
    blog_title:str
    blog_text:str
    blog_created_at:float
    blog_updated_at:float
    blog_owner_id:str
    blog_owner_username:str

class getBlogComments(BaseModel):
    comment_id:str
    owner_user_id:str
    owner_username:str
    comment_text:str
    comment_created_at:float
    comment_updated_at:float

class getBlogCommentsResponseModel(BaseModel):
    message:str
    blog_id:str
    comments:Optional[List[getBlogComments]]

class listedBlogs(BaseModel):
    blog_id:str
    blog_title:str
    blog_text:str
    blog_owner_name:str
    blog_created_at:float
    blog_updated_at:float

class listBlogsResponseModel(BaseModel):
    message:str
    listed_blogs:Optional[List[listedBlogs]]