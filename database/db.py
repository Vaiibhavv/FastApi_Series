from contextlib import contextmanager
from typing import Annotated

from dotenv import load_dotenv
import os

from fastapi import Depends 
from models.dbddltask import DbTaskModel
from sqlmodel import SQLModel, Session,create_engine
load_dotenv()


USERNAME=os.environ.get("DB_USERNAME")
PASSWORD=os.environ.get("DB_PASSWORD")
DB_URL = f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@localhost:5432/postgres"
engine=create_engine(DB_URL,echo=True)

def create_table():
    SQLModel.metadata.create_all(engine)

## each http request will be create a session
@contextmanager
def sessionHandling():
    session=Session(engine)

    try:
        yield session
    except:
        session.rollback()  ## handle if any error occurs
        raise
    finally:
        session.close()
    
def get_session():
    with sessionHandling() as session:
        yield session

## to handle the session creation and closing automatically 
SessionDependency=Annotated[Session,Depends(get_session)]
