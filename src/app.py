from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends
from src.schemas import PostCreate, PostResponse, UserRead, UserCreate, UserUpdate
from src.db import Post, create_db_and_tables, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy import select
from src.images import imagekit
import os
import shutil
import uuid
import tempfile
from src.users import auth_backend, current_active_user, fastapi_users

# Runs when the app starts and creates the database tables
@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

# FastAPI app instance
app = FastAPI(lifespan=lifespan)

app.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"])
app.include_router(fastapi_users.get_register_router(UserRead, UserCreate), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_reset_password_router(), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_verify_router(UserRead), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_users_router(UserRead,UserUpdate), prefix="/auth", tags=["auth"])

# Upload a file, send it to ImageKit, and save post details in the database
@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    caption: str = Form(""),
    session: AsyncSession = Depends(get_async_session)
):
    temp_file_path = None

    try:
        # Save the uploaded file to a temporary local file first
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            temp_file_path = temp_file.name
            shutil.copyfileobj(file.file, temp_file)

        # Open the temp file and upload it to ImageKit
        with open(temp_file_path, "rb") as f:
            upload_result = imagekit.files.upload(
                file=f,
                file_name=file.filename,
                use_unique_file_name=True,
                tags=["backend-upload"]
            )

            # Store the uploaded file info in the database
            post = Post(
                caption=caption,
                url=upload_result.url,
                file_type="video" if file.content_type.startswith("video/") else "image",
                file_name=upload_result.name
            )
            session.add(post)
            await session.commit()
            await session.refresh(post)
            return post

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # Remove the temp file and close the uploaded file handle
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        file.file.close()

# Return all posts in reverse chronological order
@app.get("/feed")
async def get_feed(
    session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(select(Post).order_by(Post.created_at.desc()))
    posts = [row[0] for row in result.all()]

    # Convert ORM objects into simple JSON-friendly dictionaries
    posts_data = []
    for post in posts:
        posts_data.append(
            {
                "id": str(post.id),
                "caption": post.caption,
                "url": post.url,
                "file_type": post.file_type,
                "file_name": post.file_name,
                "created_at": post.created_at.isoformat()
            }
        )

    return {"posts": posts_data}

# Delete a post by its ID
@app.delete("/posts/{post_id}")
async def delete_post(post_id: str, session: AsyncSession = Depends(get_async_session)):
    try:
        post_uuid = uuid.UUID(post_id)

        # Find the post first so we can delete it safely
        result = await session.execute(select(Post).where(Post.id == post_uuid))
        post = result.scalars().first()

        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        await session.delete(post)
        await session.commit()

        return {"success": True, "message": "Post deleted succesfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))