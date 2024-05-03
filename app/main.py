from fastapi import FastAPI
from .database import engine, Base
from .routers.post import post_router
from .routers.user import user_router
from .routers.auth import auth_router
from .routers.vote import vote_router
from .config import settings

from fastapi.middleware.cors import CORSMiddleware

# create tables 
# Base.metadata.create_all(bind=engine)
app = FastAPI()

origins = [
    "*"
    # "http://localhost",
    # "http://localhost:8080",
    # "https://www.google.com",
    # "https://www.youtube.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')  # Change to @app.get() decorator
async def hello():
    return {"message": "hello world, deploying on ubuntu!"}


app.include_router(post_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(vote_router)