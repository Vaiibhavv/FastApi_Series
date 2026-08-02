from pydantic import BaseModel


class TaskResponseModel(BaseModel):
    id:int
    name: str
    taskid: int
    status: str
