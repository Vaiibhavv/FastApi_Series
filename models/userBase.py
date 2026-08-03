from sqlmodel import SQLModel,Field
class UserBase(SQLModel):
    username:str=Field(min_length=2,max_length=30)
    email:str=Field(unique=True,nullable=False)
    Gender:str=Field(min_length=4,nullable=False)