from fastapi import status, HTTPException, Response, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..models import User
from ..serializers import *
from ..database import get_db
from ..utils import verify
from ..oauth2 import create_access_token

auth_router = APIRouter(prefix='/auth', tags=['Authentication'])

# List User
@auth_router.post('/login', response_model=TokenSerializer)
def authenticate(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(detail=f"Invalid Creadentials." , status_code= status.HTTP_400_BAD_REQUEST)

    if not verify(user_credentials.password, user.password):
        raise HTTPException(detail=f"Password do not match. Please provide correct password" , status_code= status.HTTP_400_BAD_REQUEST)

    # create token
    access_token = create_access_token(data = {"user_id": user.id})

    # return token
    return {"access_token": access_token, "token_type": "bearer"}