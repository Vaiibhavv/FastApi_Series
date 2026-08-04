
from pwdlib import PasswordHash
from sqlmodel import select
from database.db import SessionDependency
from models.userModel import User
from fastapi import HTTPException,status
#Initialize PasswordHash with Argon2 (recommended)
## convert the string password into the hash password
password_context = PasswordHash.recommended()

def hash_password(password: str) -> str:
    """Generates a secure hash from a plain text password."""
    return password_context.hash(password)

def validate_password(hashed_password:str,password:str)-> bool:
    return password_context.verify(hash=hashed_password,password=password)


async def check_credentials(username,password,session:SessionDependency):

    ## first will check if the user is present or not in User Model
    db_user=session.exec(select(User).where(User.username==username)).first()
    if not db_user:
        return False

    print("User Cred ",db_user)

    if not validate_password(hashed_password=db_user.password,password=password):
        return False
        #raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Wrong Credentials")

    ## if user and password is correct then return the db_user
    return db_user
        

