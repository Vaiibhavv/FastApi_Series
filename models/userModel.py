
from sqlmodel import Field, SQLModel
from datetime import datetime
from models.userBase import UserBase

class User(UserBase,table=True):
    id:int | None =Field(primary_key=True,ge=1,default=None)
    created_at:datetime=Field(datetime.now(),nullable=False)
    is_active:bool=Field(nullable=False)
    password:str=Field(nullable=False,min_length=6,max_length=120)