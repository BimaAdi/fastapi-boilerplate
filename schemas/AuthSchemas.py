from pydantic import BaseModel

class LoginRequest(BaseModel):

    username: str
    password: str

class RoleResponse(BaseModel):

    id: int
    name: str

class LoginResponse(BaseModel):

    id: int
    username: str
    role: RoleResponse
    token: str

class LogoutRequest(BaseModel):

    id: int
    username: str
    token: str

class LogoutResponse(BaseModel):

    id: int
    username: str
    role: RoleResponse
