from pydantic import BaseModel

# Pydantic model for validating post creation data
# Defines the structure and types of data expected when creating a new post
class PostCreate(BaseModel):
    title: str
    content: str

class PostResponse(BaseModel):
    title: str
    content: str