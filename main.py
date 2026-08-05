
from fastapi import FastAPI
from database.db import create_table
from routers.dbtaskmain import router as task_router
from routers.auth import user_router
from routers.users import router as user_login

app=FastAPI(title="Task Details With Postgresql",version="0.0.1")

app.include_router(task_router)
app.include_router(user_router)
app.include_router(user_login)

@app.on_event("startup")
def on_startup():
    create_table()