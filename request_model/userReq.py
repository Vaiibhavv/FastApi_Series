
from models.userBase import UserBase
from sqlmodel import Field
class UserReq(UserBase):
    password:str=Field(nullable=False,min_length=6,max_length=120)
    is_active:bool=Field(nullable=False)
