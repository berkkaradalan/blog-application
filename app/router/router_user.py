from fastapi import APIRouter, Depends,HTTPException, status
from app.models.request_models import registerRequestModel, loginDocument, editPasswordRequestModel
from app.models.response_models import registerResponseModel, getProfileDetailResponseModel, LoginToken, updateResponseModel
from  app.models.collection_models import userDocument
from app.config.helper import mongo_collections, authenticate_user, create_access_token, access_token_expire_minutes
import app.config.handler as handler
from app.config.helper import verify_password,get_current_active_user,validate_email, create_id, get_current_time, get_password_hash
from pymongo.errors import PyMongoError
from typing import Annotated
from datetime import timedelta

router = APIRouter()

@router.get("/")
async def root(current_user: Annotated[userDocument, Depends(get_current_active_user)]):
    return {"github":"github.com/bevkk"}

@router.post("/register", response_model=registerResponseModel)
async def register(register_data:registerRequestModel):
    user = mongo_collections.users.find_one({"username":register_data.username})
    if user:
        raise handler.UsernameAlreadyExistsException
    if register_data.password != register_data.password_confirm:
        raise handler.PasswordConfirmException
    if not validate_email(register_data.email):
        raise handler.EmailValidationException
    try:
        user_collection = userDocument(
            user_id=str(create_id()),
            username=register_data.username,
            name=register_data.name,
            lastname=register_data.lastname,
            email=register_data.email,
            password=get_password_hash(register_data.password),
            user_created_at=float(get_current_time()),
            user_updated_at=float(get_current_time()),
            )
        mongo_collections.users.insert_one(user_collection.model_dump())
        return {"message":"User created successfully!"}
    except PyMongoError as e:
        handler.MongoDBExceptionHandler.handle_mongo_error(e)
    except Exception as e:
        handler.UnExpectedError()

@router.post("/login", response_model=LoginToken)
async def login_for_access_token(
    form_data: loginDocument
):
    user = authenticate_user(mongo_collections.users, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"username":form_data.username,"access_token": f"Bearer {access_token}"}

@router.get("/get-profile-detail")
async def get_profile_detail(user_id:str):
    user = mongo_collections.users.find_one({"user_id":user_id})
    if not user:
        raise handler.UserNotFoundException
    try:
        return getProfileDetailResponseModel(
            user_id=user_id,
            username=user["username"],
            name=user["name"],
            lastname=user["lastname"],
            email=user["email"],
            user_created_at=user["user_created_at"],
            user_updated_at=user["user_updated_at"],
        )
    except PyMongoError as e:
        raise handler.MongoDBExceptionHandler.handle_mongo_error(e)

@router.get("/get-profile", response_model=getProfileDetailResponseModel)
async def get_profile(current_user: Annotated[userDocument, Depends(get_current_active_user)]):
    try:
        current_user_data = getProfileDetailResponseModel(
            user_id=current_user.user_id,
            username=current_user.username,
            name=current_user.name,
            lastname=current_user.lastname,
            email=current_user.email,
            user_created_at=current_user.user_created_at,
            user_updated_at=current_user.user_updated_at
        )
        return current_user_data
    except Exception as e:
        raise handler.UnExpectedError()

@router.put("/edit_password", response_model=updateResponseModel)
async def edit_password(password_data:editPasswordRequestModel,current_user: Annotated[userDocument, Depends(get_current_active_user)]):
    if not verify_password(password_data.password_old, current_user.password):
        raise handler.WrongPassword()
    if password_data.password_new is None or password_data.password_new == "":
        raise handler.PasswordValidationException()
    if password_data.password_new != password_data.password_new_confirm:
        raise handler.PasswordConfirmException()
    try:
        mongo_collections.users.update_one({"user_id":current_user.user_id}, {"$set":{"password":get_password_hash(password_data.password_new)}})
        return {"message":"Password updated successfully!"}
    except PyMongoError as e:
        raise handler.MongoDBExceptionHandler.handle_mongo_error(e)
    except Exception as e:
        raise handler.UnExpectedError()