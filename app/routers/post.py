from fastapi import status, HTTPException, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Post, Vote
from serializers import *
from database import get_db
from oauth2 import get_current_user

post_router = APIRouter(prefix='/posts', tags=['Posts'])

# List Posts
@post_router.get('/', response_model=ListPostWithVotesSerializer)
def get_posts(search: Optional[str] = '', limit: int = 10, skip: int = 0, current_user: int = Depends(get_current_user), db: Session = Depends(get_db)):
    posts_query = db.query(Post, func.count(Vote.post_id).label("votes")).outerjoin(Vote, Vote.post_id == Post.id).group_by(Post.id)

    if search:
        posts_query = posts_query.filter(Post.title.contains(search))

    posts = posts_query.limit(limit).offset(skip)
    posts = [{"post": res[0], "vote": res[1]} for res in posts]
    return {"posts": posts}

# Create Post
@post_router.post('/', status_code=status.HTTP_201_CREATED, response_model=RetrievePostSerializer)
def create_post(post: CreatePostSerializer, current_user: int = Depends(get_current_user), db: Session = Depends(get_db)):
    new_post = Post(owner_id=current_user.id, **post.__dict__)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# Retrieve Post
@post_router.get('/{post_id}', response_model=PostWithVotesSerializer)
def get_post(post_id: int, current_user: int = Depends(get_current_user), db: Session = Depends(get_db)):
    post_query = db.query(Post, func.count(Vote.post_id).label("votes")).outerjoin(Vote, Vote.post_id == Post.id).group_by(Post.id)
    post = post_query.filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {post_id} was not found.")

    return {'post': post[0], 'vote': post[1]}

# Delete Post
@post_router.delete('/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, current_user: int = Depends(get_current_user), db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {post_id} was not found.")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    
    db.delete(post)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)

# Update Post
@post_router.put('/{post_id}', response_model=RetrievePostSerializer)
def upadte_post(post_id: int, post_data: UpdatePostSerializer, current_user: int = Depends(get_current_user), db: Session = Depends(get_db)):
    update_post_query = db.query(Post).filter(Post.id == post_id)
    post = update_post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {post_id} was not found.")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    
    post_data_dict = post_data.__dict__
    post_data_dict['owner_id'] = current_user.id
    update_post_query.update(post_data_dict, synchronize_session=False)
    db.commit()
    db.flush()
    return update_post_query.first()