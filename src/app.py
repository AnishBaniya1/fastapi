from fastapi import FastAPI, HTTPException

# Create FastAPI application instance
# This is the main app object that handles all routes and requests
app = FastAPI()

# Define a GET endpoint at /hello-world
# @app.get() is a decorator that registers this function as a route handler

text_posts = {
    1: {"Title": "New Post", "Content": "Cool test post"},
    2: {"Title": "Learning Python", "Content": "Python is fun and powerful."},
    3: {"Title": "Flutter Journey", "Content": "Building beautiful mobile apps."},
    4: {"Title": "Morning Thoughts", "Content": "Start small, grow daily."},
    5: {"Title": "Tech Update", "Content": "Exploring modern dev tools."},
    6: {"Title": "AI Notes", "Content": "Machine learning is evolving fast."},
    7: {"Title": "Backend Basics", "Content": "APIs connect everything together."},
    8: {"Title": "Debug Mode", "Content": "Errors help us learn better."},
    9: {"Title": "Daily Motivation", "Content": "Consistency beats talent."},
    10: {"Title": "Code Life", "Content": "Write clean and simple code."}
}


@app.get("/posts")
def get_all_posts(limit: int = None):
    if limit:
        return list(text_posts.values())[:limit]
    return text_posts

@app.get("/posts/{id}")
def get_post(id:int):
    if id not in text_posts:
        raise HTTPException(status_code=404, detail="Post Not Found")
    return text_posts.get(id)
