from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException,status,Path,Query
from sqlmodel import Session, func, select
from models.dbddltask import DbTaskModel
from database.db import create_table,SessionDependency
from request_model.taskreq import TaskRequest
from response_model.taskresponse import TaskResponse

app=FastAPI(title="Task Details With Postgresql",version="0.0.1")

@app.on_event("startup")
def on_startup():
    create_table()

## for each db query like (select, insert the session will be create)
@app.post("/taskmodel/createtask",response_model=TaskResponse,status_code=status.HTTP_200_OK)
async def create_task(taskreq:TaskRequest,session:SessionDependency):
    task=DbTaskModel.model_validate(taskreq)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


## get all task contains in posgtgresdb

@app.get("/taskmodel/getalltask",response_model=list[TaskResponse],status_code=status.HTTP_200_OK)
async def get_alldb_task(session:SessionDependency):
    query=select(DbTaskModel)
    result=session.exec(query).all()
    return result

@app.get("/taskmodel/taskstatus",response_model=list[TaskResponse],status_code=status.HTTP_302_FOUND)
async def get_taskByStatus(session:SessionDependency,taskStatus:str=Query(description="Status should be (New, Pending,Completed, In Progress)")):
    query=select(DbTaskModel).where(func.lower(DbTaskModel.status)==taskStatus.lower())
    statusResult=session.exec(query).all()
    if not statusResult:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Status Not found")
    return statusResult

@app.get('/taskmodel/{id}',response_model=TaskResponse,status_code=status.HTTP_202_ACCEPTED)
async def get_taskById(session:SessionDependency,id:int=Path(ge=1)):
    task=session.get(DbTaskModel,id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Id not found")
    return task
@app.put("/taskmodel/update_task/{id}",response_model=TaskResponse,status_code=status.HTTP_202_ACCEPTED)
async def update_taskById(taskreq:TaskRequest, session:SessionDependency,id:int):
    task=session.get(DbTaskModel,id)
    if not task:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Id not found")
    task.status=taskreq.status
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
@app.delete("/taskmode/deletetask/{id}")
async def delete_task(session:SessionDependency,id:int=Path(ge=1)):
    task=session.get(DbTaskModel,id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Id not found")

    session.delete(task)
    session.commit()
    return f"Id {id} is Successfully Deleted"