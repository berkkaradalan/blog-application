from fastapi import APIRouter,Depends, Query
from app.models.collection_models import commentDocument,userDocument
from app.models.request_models import addCommentRequestModel
from app.models.response_models import createResponseModel,deleteResponseModel, getBlogCommentsResponseModel, getBlogComments
from app.config.helper import mongo_collections, create_id, get_current_time, get_current_active_user
import app.config.handler as handler
from typing import Annotated
from pymongo.errors import PyMongoError

router = APIRouter()

@router.get("/")
async def root():
    return {"github":"github.com/bevkk"}

@router.post("/add-comment/{blog_id}", response_model=createResponseModel)
async def add_comment(blog_id:str,comment_data:addCommentRequestModel,current_user: Annotated[userDocument, Depends(get_current_active_user)]):
    blog = mongo_collections.blogs.find_one({"blog_id":blog_id})
    if not blog:
        raise handler.BlogNotFound()
    try:
        mongo_collections.comments.insert_one(commentDocument(
            comment_id=str(create_id()),
            comment_blog_id=blog_id,
            comment_owner_id=current_user.user_id,
            comment_text=comment_data.comment_text,
            comment_created_at=get_current_time(),
            comment_updated_at=get_current_time()
        ).model_dump())
        return {"message":"Comment added succesfully!"}
    except PyMongoError as e:
        raise handler.MongoDBExceptionHandler.handle_mongo_error(e)
    except Exception as e:
        raise handler.UnExpectedError()

@router.delete("/delete-comment/{comment_id}", response_model=deleteResponseModel)
async def delete_comment(comment_id:str, current_user: Annotated[userDocument, Depends(get_current_active_user)]):
    comment = mongo_collections.comments.find_one({"comment_id":comment_id})
    if not comment:
        raise handler.CommentNotFound()
    if comment["comment_owner_id"] != current_user.user_id:
        raise handler.UnauthorizedAction()
    try:
        mongo_collections.comments.delete_one({"comment_id":comment_id})
        return {"message":"Comment deleted succesfully!"}
    except PyMongoError as e:
        raise handler.MongoDBExceptionHandler.handle_mongo_error(e)
    except Exception as e:
        raise handler.UnExpectedError()

@router.get("/get-blog-comments/{blog_id}", response_model=getBlogCommentsResponseModel)
async def get_blog_comments(blog_id:str, limit:int = Query(10), offset: int = Query(0)):
    try:
        comments_cursor = mongo_collections.comments.find({"comment_blog_id": blog_id}).skip(offset).limit(limit)
        comments = []
        for comment_cursor in comments_cursor:
            username = mongo_collections.users.find_one({"user_id":comment_cursor["comment_owner_id"]})["username"]
            comments.append(getBlogComments(
                comment_id=comment_cursor["comment_id"],
                owner_user_id=comment_cursor["comment_owner_id"],
                owner_username=username,
                comment_text=comment_cursor["comment_text"],
                comment_created_at=comment_cursor["comment_created_at"],
                comment_updated_at=comment_cursor["comment_updated_at"],
            ))
        return getBlogCommentsResponseModel(
            message=f"{len(comments)} items are listed",
            blog_id=blog_id,
            comments=comments
        ) 
    except PyMongoError as e:
        raise handler.MongoDBExceptionHandler.handle_mongo_error(e)
    except Exception as e:
        raise handler.UnExpectedError()