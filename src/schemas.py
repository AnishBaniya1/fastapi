from pydantic import BaseModel
from fastapi_users import schemas
import uuid

# Pydantic model for validating post creation data
# Defines the structure and types of data expected when creating a new post
class PostCreate(BaseModel):
    title: str
    content: str

class PostResponse(BaseModel):
    title: str
    content: str

class UserRead(schemas.BaseUser[uuid.UUID]):
    pass 

class UserCreate(schemas.BaseUserCreate):
    pass 

class UserUpdate(schemas.BaseUserUpdate):
    pass 