from fastapi import FastAPI, HTTPException
from src.schemas import PostCreate, PostResponse
from src.db import Post, create_db_and_tables, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app:FastAPI):
    await create_db_and_tables()
    yield

# Create FastAPI application instance
# This is the main app object that handles all routes and requests
app = FastAPI(lifespan=lifespan)

# Define a GET endpoint at /hello-world
# @app.get() is a decorator that registers this function as a route handler

text_posts = {
    1: {"title": "New Post", "Content": "Cool test post"},
    2: {"title": "Learning Python", "Content": "Python is fun and powerful."},
    3: {"title": "Flutter Journey", "Content": "Building beautiful mobile apps."},
    4: {"title": "Morning Thoughts", "Content": "Start small, grow daily."},
    5: {"title": "Tech Update", "Content": "Exploring modern dev tools."},
    6: {"title": "AI Notes", "Content": "Machine learning is evolving fast."},
    7: {"title": "Backend Basics", "Content": "APIs connect everything together."},
    8: {"title": "Debug Mode", "Content": "Errors help us learn better."},
    9: {"title": "Daily Motivation", "Content": "Consistency beats talent."},
    10: {"title": "Code Life", "Content": "Write clean and simple code."}
}


@app.get("/posts")
def get_all_posts(limit: int = None):
    if limit:
        return list(text_posts.values())[:limit]
    return text_posts

@app.get("/posts/{id}") #path param
def get_post(id:int):
    if id not in text_posts:
        raise HTTPException(status_code=404, detail="Post Not Found")
    return text_posts.get(id)

@app.post("/posts")
def create_post(post:PostCreate) -> PostResponse:
    new_post={"title":post.title, "Content":post.content}
    text_posts[max(text_posts.keys())+1]=new_post
    return new_post
