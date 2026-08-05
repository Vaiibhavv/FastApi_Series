
## Changed password endpoint for a current user

from typing import Annotated
from models.userModel import User
from fastapi import APIRouter, Depends, HTTPException, status
from database.db import SessionDependency
from request_model.passwordChangeReq import PasswordChangedReq
from utilities.utilities import hash_password, validate_password, validate_token

router=APIRouter(tags=["Change Password"])

auth_user_dependency=Annotated[dict,Depends(validate_token)]

@router.put("/user/changedpassword")
def userChange_password(userReq:PasswordChangedReq,user:auth_user_dependency,session:SessionDependency):

    ## check if user is valid or not
    if user is None:
        raise HTTPException (status_code=status.HTTP_401_UNAUTHORIZED,detail="Unauthorized User")

    ## check if user is present or not in db
    db_user=session.get(User,user.get("id"))
    if db_user is None:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND,detail="User not found")

    ## check the db password is matching or not with current_password
    db_password=db_user.password
    isSame=validate_password(hashed_password=db_user.password,password=userReq.current_password)

    if isSame is None:
        return HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="Your Current password is incorrect !")

    #if match then update the current password with new password
    db_user.password=hash_password(userReq.new_password)
    session.add(db_user)
    session.commit()
    return {"message": "Password Changed!!!"}