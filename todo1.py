from fastapi import FastAPI, Body

## first create the application 
app= FastAPI()

## todos task 

task_list =[
    {"title":"task 1", "item":["Add the new module id", "json workflow","map workflow with enrich"],"is_completed":True},
    {"title":"task 2", "item":["Add assets enrichemnt","add descritptor enrich"],"is_completed":False},
    {"title":"task 3", "item":["Create the new Module Automation Pipeline","Add sparkjob and kafka topic component"],"is_completed":False}
]

@app.get("/")
def fastStarted():
    return "Api launched"

#second get api to show all tasks

@app.get("/tasklist")
def taskList():
    return task_list

# post api 
@app.post("/tasklist/createtask")
def add_task(new_task=Body()):
    task_list.append(new_task)

    return {"message":"Success"}

# put api 
@app.put("/tasklist/updatetask")
def update_task(task_update=Body()):
    task_list[0]['task1'][0]=task_update
    return {"message":"Success"}

## path variable example 
@app.delete("/tasklist/{title}")
def delete_task(title):
    for index in range(len(task_list)):
        if task_list[index]['title'].lower()==title.lower():
            task_list.pop(index)
            return {"message":"Success"}


## query parameter is ( key value getting from user)
# eg. http://localhost/task?key=value 
@app.get("/task/completed")
def task_status(is_completed:bool):
    result=[]
    for i in range(len(task_list)):
        if task_list[i]['is_completed']==is_completed:
            result.append(task_list[i])
    return result
