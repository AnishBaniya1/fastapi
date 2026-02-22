from fastapi import FastAPI

# Create FastAPI application instance
# This is the main app object that handles all routes and requests
app = FastAPI()

# Define a GET endpoint at /hello-world
# @app.get() is a decorator that registers this function as a route handler
# When someone visits http://localhost:8000/hello-world, this function runs
@app.get("/hello-world")
def hello_world():
     # FastAPI automatically converts Python dictionaries to JSON responses
    return {"message":"Hello World"} #return dictionary as JSON
