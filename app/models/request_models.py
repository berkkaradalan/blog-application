from pydantic import BaseModel
from typing import Optional

class createBlogRequestModel(BaseModel):
    blog_title:str
    blog_text:str

class registerRequestModel(BaseModel):
    username:str
    name:str
    lastname:str
    email:str
    password:str
    password_confirm:str

class loginDocument(BaseModel):
    username:str
    password:str

class addCommentRequestModel(BaseModel):
    comment_text:str

class editPasswordRequestModel(BaseModel):
    password_old:str
    password_new:str
    password_new_confirm:str

class editBlogRequestModel(BaseModel):
    blog_title:Optional[str] | None = None
    blog_text:Optional[str] | None = None