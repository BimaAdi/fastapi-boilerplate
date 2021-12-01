from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from common.responses_schemas import (
    NotFound, NoContent,
    BadRequest, InternalServerError
)
from common.responses_services import common_response
from common.security import oauth2_scheme, get_user_from_jwt_token
from schemas.UserSchemas import (
    GetAllUserResponse, GetUserResponse, 
    UserCreateRequest, UserUpdateRequest
)
from services.UserServices import UserServices

router = APIRouter(
    prefix='/user',
    tags=['user']
)

@router.get('/', responses={
    '200': { 'model': GetAllUserResponse},
    '500': { 'model': InternalServerError}
})
async def get_all_user(page:int, page_size:int, token: str = Depends(oauth2_scheme)):
    request_user = get_user_from_jwt_token(token)
    users = await UserServices.get_all_user(request_user=request_user, page=page, page_size=page_size)
    return common_response(users)


@router.get('/{id}', responses={
    '200': {'model': GetUserResponse},
    '404': {'model': NotFound}
})
async def get_detail_user(id: int, token: str = Depends(oauth2_scheme)):
    request_user = get_user_from_jwt_token(token)
    user_detail = await UserServices.get_detail_user(request_user=request_user, id=id)
    return common_response(user_detail)

@router.post('/', responses={
    '201': {'model': GetUserResponse},
    '400': {'model': BadRequest},
    '500': {'model': InternalServerError}
})
async def create_user(request: UserCreateRequest, token: str = Depends(oauth2_scheme)):
    request_user = get_user_from_jwt_token(token)
    new_user = await UserServices.create_user(request_user=request_user, data=request)
    return common_response(new_user)

@router.put('/{id}', responses={
    '200': {'model': GetUserResponse},
    '400': {'model': BadRequest},
    '404': {'model': NotFound},
    '500': {'model': InternalServerError}
})
async def update_user(id: int, request: UserUpdateRequest, token: str = Depends(oauth2_scheme)):
    request_user = get_user_from_jwt_token(token)
    updated_user = await UserServices.update_user(request_user=request_user, id=id, data=request)
    return common_response(updated_user)

@router.delete('/{id}', responses={
    '204': {'model': NoContent},
    '400': {'model': BadRequest},
    '404': {'model': NotFound},
    '500': {'model': InternalServerError}
})
async def delete_user(id: int, token: str = Depends(oauth2_scheme)):
    request_user = get_user_from_jwt_token(token)
    res = await UserServices.delete_user(request_user=request_user, id=id)
    return common_response(res)
