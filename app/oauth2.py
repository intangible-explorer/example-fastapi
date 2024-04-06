from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime,timedelta
from serializers import TokenDataSerializer
from fastapi.security import OAuth2PasswordBearer
from database import get_db
from models import User
from config import settings

oauth2_sceme = OAuth2PasswordBearer(tokenUrl='/auth/login')

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get('user_id')

        if user_id is None:
            raise credentials_exception

        token_data = TokenDataSerializer(id=user_id)
    except JWTError as e:
        raise credentials_exception

    return token_data

def get_current_user(token: str = Depends(oauth2_sceme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    token_data = verify_access_token(token, credentials_exception)

    user = db.query(User).filter(User.id == token_data.id).first()
    if not user:
        raise HTTPException(detail=f"User with id: {token_data.id} does not exist.", status_code=status.HTTP_400_BAD_REQUEST)
    return user