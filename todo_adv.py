from fastapi import FastAPI,Body, Path, Query,HTTPException,status
from taskModel import TaskClass
from tasreqvalidator import TaskReqValidator
from taskResponseModel import TaskResponseModel
app=FastAPI(title="Task Module Api")

tasklist=[
    TaskClass(1,"Suresh kumar",1323,"New"),
    TaskClass(2,"Jayesh pandey",1423,"Pending"),
    TaskClass(3,"Mahesh sharma",1522,"In progress"),
    TaskClass(4,"Rakesh vasant",1821,"Completed")
]


@app.get("/tasklist/",response_model=list[TaskResponseModel],status_code=status.HTTP_200_OK) #
async def EmpTask():
    return tasklist

## add the task with validation
# @app.post("/tasklist/create")
# async def addTask(task:TaskReqValidator):
#     t=TaskClass(**task.dict())
#     tasklist.append(get_taskid(t))
#     return t 

# def get_taskid(task):
#     if len(tasklist)==0:
#         task.id=1
#     else:
#         task.id=tasklist[-1].id+1
#     return task
    
@app.post("/tasklist/createtask",status_code=status.HTTP_201_CREATED)
async def create_task(task:TaskReqValidator):
    t=TaskClass(**task.dict())
    tasklist.append(get_length(t))
    return t

def get_length(task):
    if len(tasklist)==0:
        task.id=1
    else:
        task.id=tasklist[-1].id+1
    return task

## update task status
@app.put("/tasklist/update",status_code=status.HTTP_302_FOUND)
async def update_task(task:TaskReqValidator):
    t=TaskClass(**task.dict())
    not_found=True ## to handle the , if id not found 
    for index in range(len(tasklist)):
        if tasklist[index].id==t.id:
            tasklist[index]=t
            return t
    if not_found:
        raise HTTPException(status_code=404,detail="Task id is not found")

## delete the task based on id 
@app.delete("/tasklist/delete/{id}",status_code=status.HTTP_202_ACCEPTED)
async def delete_task(id:int=Path(ge=1,le=len(tasklist))):
    not_found=True ## to handle if id not found 
    for index in range(len(tasklist)):
        if tasklist[index].id==id:
            tasklist.pop(index)
            return {"message":"id deleted successfully"}
    if not_found:
        raise HTTPException(status_code=404,detail="Task id is not found")

## get the task based on the status 
@app.get("/tasklist/taskstatus")
async def get_task_status(status:str=Query(description="Status Should be in (In progress, Pending, New, Completed)")):
    for index in range(len(tasklist)):
        if tasklist[index].status.lower()==status.lower():
            return tasklist[index]
