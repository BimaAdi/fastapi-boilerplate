from typing import List
from pydantic import BaseModel, Field

class GetRoleResponse(BaseModel):

    id: int
    name: str

class GetAllRoleResponse(BaseModel):

    page: int
    pageSize: int
    totalPage: int
    count: int
    data: List[GetRoleResponse]

class CreateRoleRequest(BaseModel):

    name: str

class UpdateRoleRequest(BaseModel):

    name: str
