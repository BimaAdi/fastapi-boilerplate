from fastapi import APIRouter, Response
from fastapi.responses import JSONResponse
from common.responses_model import (
    NotFound, NoContent,
    BadRequest, InternalServerError
)
from common.responses_services import common_response
from serializers.UserSerializers import (
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
async def get_all_user():
    users = await UserServices.get_all_user(page=1, pageSize=5)
    return common_response(users)


@router.get('/{id}', responses={
    '200': {'model': GetUserResponse},
    '404': {'model': NotFound}
})
async def get_detail_user(id: int):
    user_detail = await UserServices.get_detail_user(id)
    return common_response(user_detail)

@router.post('/', responses={
    '201': {'model': GetUserResponse},
    '400': {'model': BadRequest},
    '500': {'model': InternalServerError}
})
async def create_user(request: UserCreateRequest):
    new_user = await UserServices.create_user(request)
    return common_response(new_user)

@router.put('/{id}', responses={
    '200': {'model': GetUserResponse},
    '400': {'model': BadRequest},
    '404': {'model': NotFound},
    '500': {'model': InternalServerError}
})
async def update_user(id: int, request: UserUpdateRequest):
    updated_user = await UserServices.update_user(id, request)
    return common_response(updated_user)

@router.delete('/{id}', responses={
    '204': {'model': NoContent},
    '404': {'model': NotFound},
    '500': {'model': InternalServerError}
})
async def delete_user(id: int):
    res = await UserServices.delete_user(id)
    return common_response(res)