from fastapi import status, HTTPException, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from ..models import *
from ..serializers import *
from ..database import get_db
from ..oauth2 import get_current_user


vote_router = APIRouter(prefix='/vote', tags=['Vote'])

@vote_router.post(path='/', status_code=status.HTTP_201_CREATED)
def vote(vote: VoteSerializer, current_user: int = Depends(get_current_user), db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {vote.post_id} does not exist")


    vote_query = db.query(Vote).filter(Vote.post_id == vote.post_id, Vote.user_id == current_user.id)

    found_vote = vote_query.first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} already voted on post {vote.post_id}")
        
        new_vote = Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote does not exist")

        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Successfully deleted vote"}