from fastapi import status, HTTPException, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from models import User
from serializers import *
from database import get_db
from utils import hash_password

user_router = APIRouter(prefix='/users', tags=['Users'])

# List User
@user_router.get('/', response_model=ListUserSerializer)
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return {"users": users}

# Create User
@user_router.post('/', status_code=status.HTTP_201_CREATED, response_model=RetrieveUserSerializer)
def create_post(user: CreateUserSerializer, db: Session = Depends(get_db)):    
    # hash the password
    hashed_password = hash_password(user.password)
    user.password = hashed_password

    new_user = User(**user.__dict__)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Retrieve User
@user_router.get('/{user_id}', response_model=RetrieveUserSerializer)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with {user_id} does not exist.")
    return user

# Delete user
@user_router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with {user_id} was not found.")
    db.delete(user)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)

# Update user
@user_router.put('/{user_id}', response_model=RetrieveUserSerializer)
def upadte_user(user_id: int, user_data: UpdateUserSerializer, db: Session = Depends(get_db)):
    update_user_query = db.query(User).filter(User.id == user_id)
    user = update_user_query.first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with {user_id} was not found.")
    
    update_user_query.update(user_data.__dict__, synchronize_session=False)
    db.commit()
    db.flush()
    return update_user_query.first()

