from typing import List, Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime


# user
class UserBase(BaseModel):
    email: EmailStr
    password: str

class CreateUserSerializer(UserBase):
    pass

class UpdateUserSerializer(UserBase):
    pass

class RetrieveUserSerializer(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

class ListUserSerializer(BaseModel):
    users: List[RetrieveUserSerializer]

    class Config:
        from_attributes = True

# Login
class TokenSerializer(BaseModel):
    access_token: str
    token_type: str

class TokenDataSerializer(BaseModel):
    id: Optional[int] = None


# Post
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class CreatePostSerializer(PostBase):
    pass

class UpdatePostSerializer(PostBase):
    pass

class RetrievePostSerializer(BaseModel):
    id: int
    title: str
    content: str
    published: bool = True
    created_at: datetime
    owner_id: int
    owner: RetrieveUserSerializer

    class Config:
        from_attributes = True

class ListPostSerializer(BaseModel):
    posts: List[RetrievePostSerializer]

    class Config:
        from_attributes = True

class PostWithVotesSerializer(BaseModel):
    post: RetrievePostSerializer
    vote: int

    class Config:
        from_attributes = True

class ListPostWithVotesSerializer(BaseModel):
    posts: List[PostWithVotesSerializer]

    class Config:
        from_attributes = True


# vote
class VoteSerializer(BaseModel):
    post_id: int
    dir: int