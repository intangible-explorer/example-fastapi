from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"
# engine : to connect to db
engine = create_engine(url=SQLALCHEMY_DATABASE_URL)

# sessionmaker : to talk to db once connected
sessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

# declarative_base : to create db models using python classes
Base = declarative_base()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()