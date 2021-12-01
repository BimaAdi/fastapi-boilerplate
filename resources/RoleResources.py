from fastapi import APIRouter, Depends
from common.responses_schemas import (
    NotFound, NoContent,
    BadRequest, InternalServerError
)
from common.responses_services import common_response
from common.security import oauth2_scheme, get_user_from_jwt_token
from schemas.RoleSchemas import (
    GetAllRoleResponse,
    GetRoleResponse,
    CreateRoleRequest,
    UpdateRoleRequest
)
from services.RoleServices import RoleServices

router = APIRouter(
    prefix='/role',
    tags=['role']
)

@router.get('/', responses={
    '200': { 'model': GetAllRoleResponse},
    '500': { 'model': InternalServerError}
})
async def get_all_role(page:int, page_size:int, token: str = Depends(oauth2_scheme)):
    request_user = get_user_from_jwt_token(token)
    result = await RoleServices.get_all_roles(request_user=request_user, page=page, page_size=page_size)
    return common_response(result)

@router.get('/{id}', responses={
    '200': {'model': GetRoleResponse},
    '404': {'model': NotFound},
    '500': {'model': InternalServerError}
})
async def get_detail_role(id: int, token: str = Depends(oauth2_scheme)):
    request_user = get_user_from_jwt_token(token)
    result = await RoleServices.get_detail_role(request_user=request_user, id=id)
    return common_response(result)

@router.post('/', responses={
    '201': {'model': GetRoleResponse},
    '500': {'model': InternalServerError}
})
async def create_role(request: CreateRoleRequest, token: str = Depends(oauth2_scheme)):
    request_user = get_user_from_jwt_token(token)
    result = await RoleServices.create_role(request_user=request_user, data=request)
    return common_response(result)

@router.put('/{id}', responses={
    '200': {'model': GetRoleResponse},
    '404': {'model': NotFound},
    '500': {'model': InternalServerError}
})
async def update_role(id: int, request: UpdateRoleRequest, token: str = Depends(oauth2_scheme)):
    request_user = get_user_from_jwt_token(token)
    result = await RoleServices.update_role(request_user=request_user, id=id, data=request)
    return common_response(result)

@router.delete('/{id}', responses={
    '204': {'model': NoContent},
    '500': {'model': InternalServerError}
})
async def delete_role(id: int, token: str = Depends(oauth2_scheme)):
    request_user = get_user_from_jwt_token(token)
    result = await RoleServices.delete_role(request_user=request_user, id=id)
    return common_response(result)
