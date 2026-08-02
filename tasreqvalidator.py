from typing import Optional
from pydantic import BaseModel, Field
# from datetime import datetime


# class TaskReqValidator(BaseModel):
#     id: Optional[int] = Field(ge=1, description="Id while creating th new task",default=None)
#     name: str = Field(min_length=2,max_length=20)
#     taskid: int = Field(ge=2)
#     status: str = Field(min_length=2,max_length=20)

class TaskReqValidator(BaseModel):
    id:Optional[int]=Field(ge=1, description="Id while creating th new task",default=None)
    name:str=Field(min_length=2,max_length=100)
    taskid:int=Field(ge=1)
    status:str=Field(min_length=1, max_length=20)

    model_config={
        "json_schema_extra":{
            "example":{
                "id":"Primary key",
                "name":"Employee Name",
                "taskid":"Task id",
                "status":"Task Status ( New, In pgrogress, Pending, Completed)"
            }
        }
    }