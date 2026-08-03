from fastapi import APIRouter,status,HTTPException
from models.userModel import User
from response_model.userResponse import UserResponse
from request_model.userReq import UserReq
from database.db import SessionDependency
from sqlmodel import select
from pwdlib import PasswordHash



user_router=APIRouter(tags=['Users'])

## encrypt the password

# Initialize PasswordHash with Argon2 (recommended)
password_context = PasswordHash.recommended()

def hash_password(password: str) -> str:
    """Generates a secure hash from a plain text password."""
    return password_context.hash(password)

@user_router.get("/auth/users",response_model=list[UserResponse],status_code=status.HTTP_200_OK)
def alluser(session:SessionDependency):
    query=select(User)
    return session.exec(query).all()

## create a user 
@user_router.post("/auth/create_user",response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(userReq:UserReq,session:SessionDependency):
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
