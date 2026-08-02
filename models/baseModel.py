from sqlmodel import SQLModel,Field

class TaskBaseModel(SQLModel):
    name:str=Field(min_length=2,max_length=100,nullable=False)
    taskid:int=Field(ge=1,nullable=False)
    status:str=Field(min_length=1, max_length=20,nullable=False)