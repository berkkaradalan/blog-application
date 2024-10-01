from fastapi import APIRouter, Depends, Query
from typing import Annotated
from app.models.request_models import createBlogRequestModel, editBlogRequestModel
from app.models.response_models import listBlogsResponseModel,getBlogDetailResponseModel, createResponseModel, deleteResponseModel, listedBlogs
from app.models.collection_models import userDocument,blogDocument
from app.config.helper import create_id, get_current_time, get_current_active_user, mongo_collections
from pymongo.errors import PyMongoError
import app.config.handler as handler

router = APIRouter()

@router.get("/")
async def root():
    return {"github":"github.com/bevkk"}

@router.post("/create-blog", response_model=createResponseModel)
async def create_blog(blog_data:createBlogRequestModel,current_user: Annotated[userDocument, Depends(get_current_active_user)]):
    try:
        blog = blogDocument(
        blog_id=str(create_id()),
        blog_owner_id=current_user.user_id,
        blog_title=blog_data.blog_title,
        blog_text=blog_data.blog_text,
        blog_created_at=float(get_current_time()),
        blog_updated_at=float(get_current_time())
    )
        mongo_collections.blogs.insert_one(blog.model_dump())
        return {"message":"Blog created successfully!"}
    except PyMongoError as e:
        raise handler.MongoDBExceptionHandler.handle_mongo_error(e)
    except Exception as e:
        raise handler.UnExpectedError()
    return blog

@router.get("/get-blog-detail/{blog_id}", response_model=getBlogDetailResponseModel)
async def get_blog_detail(blog_id:str):
    try:
        blog = mongo_collections.blogs.find_one({"blog_id":blog_id})
        if not blog:
            raise handler.BlogNotFound()
        user = mongo_collections.users.find_one({"user_id":blog["blog_owner_id"]})
        return getBlogDetailResponseModel(
            blog_title=blog["blog_title"],
            blog_text=blog["blog_text"],
            blog_created_at=blog["blog_created_at"],
            blog_updated_at=blog["blog_updated_at"],
            blog_owner_id=blog["blog_owner_id"],
            blog_owner_username=user["username"]
        )
    except PyMongoError as e:
        raise handler.MongoDBExceptionHandler.handle_mongo_error(e)
    except Exception as e:
        raise handler.UnExpectedError()

@router.delete("/delete-blog/{blog_id}", response_model=deleteResponseModel)
async def delete_blog(blog_id:str, current_user: Annotated[userDocument, Depends(get_current_active_user)] ):
    try:
        blog = mongo_collections.blogs.find_one({"blog_id":blog_id})
        if not blog:
            raise handler.BlogNotFound()
        mongo_collections.blogs.delete_one({"blog_id":blog_id})
        mongo_collections.comments.delete_many({"comment_blog_id":blog_id})
        return {"message":"Blog deleted successfully!"}
    except PyMongoError as e:
        raise handler.MongoDBExceptionHandler.handle_mongo_error(e)
    except Exception as e:
        raise handler.UnExpectedError()

@router.get("/list-blogs", response_model=listBlogsResponseModel)
async def list_blogs(limit:int = Query(10), offset: int = Query(0)):
    try:
        blogs =  mongo_collections.blogs.find().skip(offset).limit(limit)
        listed_blogs = []
        for blog in blogs:
            blog_owner_name = mongo_collections.users.find_one({"user_id":blog["blog_owner_id"]})["username"]
            listed_blogs.append(listedBlogs(
                blog_id=blog["blog_id"],
                blog_title=blog["blog_title"],
                blog_text=blog["blog_text"],
                blog_owner_name=blog_owner_name,
                blog_created_at=blog["blog_created_at"],
                blog_updated_at=blog["blog_updated_at"]
            ))
        return listBlogsResponseModel(
            message=f"{len(listed_blogs)} items are listed.",
            listed_blogs=listed_blogs,
        )
    except PyMongoError as e:
        raise handler.MongoDBExceptionHandler.handle_mongo_error(e)
    except Exception as e:
        raise handler.UnExpectedError()

@router.put("/update-blog/{blog_id}")
async def update_blog(blog_id:str, blog_data:editBlogRequestModel,current_user: Annotated[userDocument, Depends(get_current_active_user)]):
    try:
        blog = mongo_collections.blogs.find_one({"blog_id":blog_id})
        if not blog:
            raise handler.BlogNotFound()
        update_data = {}
        if blog_data.blog_title is not None and blog_data.blog_title != "":
            update_data["blog_title"] = blog_data.blog_title
        if blog_data.blog_text is not None and blog_data.blog_text != "":
            update_data["blog_text"] = blog_data.blog_text
        if update_data:
            update_data["blog_updated_at"] = float(get_current_time())
        mongo_collections.blogs.update_one({"blog_id":blog_id},{"$set":update_data})
        return {"message":"Blog updated successfully!"}

    except PyMongoError as e:
        raise handler.MongoDBExceptionHandler.handle_mongo_error(e) 
    except Exception as e:
        raise handler.UnExpectedError()