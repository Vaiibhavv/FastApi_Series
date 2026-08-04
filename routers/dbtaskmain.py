
from fastapi import APIRouter,  HTTPException,status,Path,Query,Depends
from sqlmodel import Session, func, select
from models.dbddltask import DbTaskModel
from database.db import SessionDependency
from request_model.taskreq import TaskRequest
from response_model.taskresponse import TaskResponse
from typing import Annotated
from utilities.utilities import validate_token

router=APIRouter(tags=["Tasks Enpoint"])

## for each db query like (select, insert the session will be create)

## last commit - create the tasks based on the user 

## create user jwt authentication validation (Dependecy Injection) 
auth_user_dependency=Annotated[dict,Depends(validate_token)]

@router.post("/taskmodel/createtask",response_model=TaskResponse,status_code=status.HTTP_200_OK)
async def create_task(taskreq:TaskRequest,user:auth_user_dependency, session:SessionDependency):

    ## check if user exist or not
    if user is None:
        raise HTTPException (status_code=status.HTTP_401_UNAUTHORIZED,detail="Unauthorized User")
    
    user_task=taskreq.model_dump()
    user_task['user_id']=user.get("id")
    task=DbTaskModel.model_validate(user_task)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


## get all task contains in posgtgresdb

@router.get("/taskmodel/getalltask",response_model=list[TaskResponse],status_code=status.HTTP_200_OK)
async def get_alldb_task(session:SessionDependency,user:auth_user_dependency):
    if user is None:
        raise HTTPException (status_code=status.HTTP_401_UNAUTHORIZED,detail="Unauthorized User")

    query=select(DbTaskModel).where(DbTaskModel.user_id==user.get('id'))
    result=session.exec(query).all()
    return result

@router.get("/taskmodel/taskstatus",response_model=list[TaskResponse],status_code=status.HTTP_302_FOUND)
async def get_taskByStatus(session:SessionDependency,user:auth_user_dependency, taskStatus:str=Query(description="Status should be (New, Pending,Completed, In Progress)")):

    if user is None:
            raise HTTPException (status_code=status.HTTP_401_UNAUTHORIZED,detail="Unauthorized User")
    
    query=select(DbTaskModel).where((func.lower(DbTaskModel.status)==taskStatus.lower()) and DbTaskModel.user_id==user.get('id'))
    statusResult=session.exec(query).all()
    if not statusResult:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Status Not found")
    return statusResult

@router.get('/taskmodel/{id}',response_model=TaskResponse,status_code=status.HTTP_202_ACCEPTED)
async def get_taskById(session:SessionDependency,user:auth_user_dependency, id:int=Path(ge=1)):

    if user is None:
        raise HTTPException (status_code=status.HTTP_401_UNAUTHORIZED,detail="Unauthorized User")

    #task=session.get(DbTaskModel,id)
    query=select(DbTaskModel).where((DbTaskModel.id==id ) and DbTaskModel.user_id==user.get('id'))
    task=session.exec(query).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Id not found")
    return task

@router.put("/taskmodel/update_task/{id}",response_model=TaskResponse,status_code=status.HTTP_202_ACCEPTED)
async def update_taskById(taskreq:TaskRequest,user:auth_user_dependency, session:SessionDependency,id:int):

    if user is None:
        raise HTTPException (status_code=status.HTTP_401_UNAUTHORIZED,detail="Unauthorized User")

    #task=session.get(DbTaskModel,id)
    query=select(DbTaskModel).where((DbTaskModel.id==id ) and DbTaskModel.user_id==user.get('id'))
    task=session.exec(query).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Id not found")
    task.status=taskreq.status
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
@router.delete("/taskmode/deletetask/{id}")
async def delete_task(session:SessionDependency,user:auth_user_dependency,id:int=Path(ge=1)):

    if user is None:
        raise HTTPException (status_code=status.HTTP_401_UNAUTHORIZED,detail="Unauthorized User")
    
    query=select(DbTaskModel).where((DbTaskModel.id==id ) and DbTaskModel.user_id==user.get('id'))
    task=session.exec(query).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Id not found")

    session.delete(task)
    session.commit()
    return f"Id {id} is Successfully Deleted"