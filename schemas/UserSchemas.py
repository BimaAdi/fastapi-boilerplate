from typing import List
from pydantic import BaseModel

class GetUserResponse(BaseModel):

    id: int
    username: str
    role_id: int

class GetAllUserResponse(BaseModel):

    page: int
    pageSize: int
    totalPage: int
    data: List[GetUserResponse]

class UserCreateRequest(BaseModel):

    username: str
    password: str
    confirm_password:str
    role_id: int

class UserUpdateRequest(BaseModel):

    username: str
    old_password: str
    new_password: str
    confirm_new_password:str
    role_id: int
