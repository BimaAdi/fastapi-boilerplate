from fastapi import APIRouter
from common.responses_model import (
    NotFound, NoContent,
    BadRequest, InternalServerError
)
from common.responses_services import common_response
from serializers.RoleSerializers import (
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
async def get_all_role(page:int, page_size:int):
    result = await RoleServices.get_all_roles(page=page, page_size=page_size)
    return common_response(result)

@router.get('/{id}', responses={
    '200': {'model': GetRoleResponse},
    '404': {'model': NotFound},
    '500': {'model': InternalServerError}
})
async def get_detail_role(id: int):
    result = await RoleServices.get_detail_role(id)
    return common_response(result)

@router.post('/', responses={
    '201': {'model': GetRoleResponse},
    '500': {'model': InternalServerError}
})
async def create_role(request: CreateRoleRequest):
    result = await RoleServices.create_role(request)
    return common_response(result)

@router.put('/{id}', responses={
    '200': {'model': GetRoleResponse},
    '404': {'model': NotFound},
    '500': {'model': InternalServerError}
})
async def update_role(id: int, request: UpdateRoleRequest):
    result = await RoleServices.update_role(id, request)
    return common_response(result)

@router.delete('/{id}', responses={
    '204': {'model': NoContent},
    '500': {'model': InternalServerError}
})
async def delete_role(id: int):
    result = await RoleServices.delete_role(id=id)
    return common_response(result)
