from fastapi import FastAPI
from app.router.router_blog import router as blog_router
from app.router.router_user import router as user_router
from app.router.router_comments import router as comment_router
from app.config.helper import mongo_manager
from fastapi.middleware.cors import CORSMiddleware
from app.config.dotenv import settings

app = FastAPI()

@app.on_event("startup")
async def startup():
    mongo_manager()

origins = settings.CORS_ALLOWED_ORIGINS

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins.split(",") if origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(blog_router, prefix="/blog", tags=["blog-endpoints"])
app.include_router(user_router, prefix="/user", tags=["user-endpoints"])
app.include_router(comment_router, prefix="/comments", tags=["comment-endpoints"])