
from pwdlib import PasswordHash
from sqlmodel import select
from database.db import SessionDependency
from models.userModel import User
from fastapi import HTTPException,status
from datetime import datetime, timedelta,timezone
from jose import jwt
import os
from dotenv import load_dotenv
load_dotenv()

## for jwt algorith and jwt secret 
JWT_SECRET = os.getenv('JWT_SECRET', '')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')


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

async def check_jwt_token(data:dict,expiry_time:timedelta):
    #create a copy 
    to_encode=data.copy()

    expire = datetime.now(timezone.utc) + expiry_time
    ## we need to add the expiry time in jwt payload 
    to_encode.update({"exp":expire})


    access_token = jwt.encode(claims=to_encode, algorithm=JWT_ALGORITHM, key=JWT_SECRET)

    return {"access_token": access_token, "token_type": "bearer"}


        

