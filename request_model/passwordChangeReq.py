
from pydantic import BaseModel
class PasswordChangedReq(BaseModel):
    current_password:str
    new_password:str