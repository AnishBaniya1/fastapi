import uvicorn
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


if  __name__ == "__main__":
    # Get port from .env file, default to 8000 if not found
    port = int(os.getenv("PORT",8000))

    uvicorn.run("src.app:app", host="localhost", port=port, reload=True)
    # Run the FastAPI application
    # "src.app:app" - path to the FastAPI app instance (src/app.py file, app variable)
    # host="localhost" - only accessible from this machine (not from network)
    # port=port - uses the port from .env file
    # reload=True - auto-reloads server when code changes (for development only)