from fastapi import APIRouter,status,HTTPException,Depends
from models.userModel import User
from response_model.userResponse import UserResponse
from request_model.userReq import UserReq
from database.db import SessionDependency
from sqlmodel import select
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from datetime import timedelta


user_router=APIRouter(tags=['Users'],prefix="/auth")

## encrypt the password
from utilities.utilities import check_credentials, check_jwt_token, hash_password
# 


@user_router.get("/users",response_model=list[UserResponse],status_code=status.HTTP_200_OK)
async def alluser(session:SessionDependency):
    query=select(User)
    return session.exec(query).all()

## create a user 
@user_router.post("/create_user",response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(userReq:UserReq,session:SessionDependency):
    """ while creating the user , first we need to check if the user already exist or not, b
    based on the email """
    user=User.model_validate(userReq)

    existing_user=session.exec(select(User).where(User.email==user.email)).first()
    print(existing_user)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED,detail="email already exist")

    user.password=hash_password(user.password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

## login the existing user
@user_router.post("/userlogin")
async def login_credential(form_data:Annotated[OAuth2PasswordRequestForm, Depends()],session:SessionDependency):
    username=form_data.username
    password=form_data.password

    ## check if the username,email is present or not in db 
    user_cred= await check_credentials(username,password,session)
    if not user_cred:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Wrong Credentials")

    data = {
        'sub': user_cred.username,
        'id': user_cred.id,
        'name': user_cred.email
    }

    token_dict=await check_jwt_token(data,timedelta(15))

    return token_dict