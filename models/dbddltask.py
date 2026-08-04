from sqlmodel import SQLModel,Field
from datetime import datetime
from models.baseModel import TaskBaseModel
class DbTaskModel(TaskBaseModel,table=True):
    id:int | None=Field(primary_key=True,ge=1, description="Id while creating th new task",default=None)
    created_at:datetime=Field(datetime.now(),nullable=False)
    user_id:int=Field(foreign_key="user.id")