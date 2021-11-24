from typing import Union
from common.responses_services import ( 
    InternalServerError, NoContent, Ok, 
    NotFound, Created
)
from repository.RoleRepository import RoleRepository
from serializers.RoleSerializers import CreateRoleRequest, UpdateRoleRequest

class RoleServices():

    @staticmethod
    async def get_all_roles(page: int, page_size: int)->Union[Ok, InternalServerError]:
        try:
            roles, count, num_page = RoleRepository.get_all_roles(page=page, page_size=page_size)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return InternalServerError(error=str(e))
        return Ok(data={
            'page': page,
            'page_size': page_size,
            'totalPage': num_page,
            'count': count,
            'data': [{'id': item.id, 'name': item.name } for item in roles]
        })

    @staticmethod
    async def get_detail_role(id: int)->Union[Ok, NotFound, InternalServerError]:
        try:
            role = RoleRepository.get_detail_role(id)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return InternalServerError(error=str(e))
        
        if role:
            return Ok(data={
                'id': role.id,
                'name': role.name
            })
        else:
            return NotFound(message=f'role with id {id} not found')

    @staticmethod
    async def create_role(data: CreateRoleRequest)->Union[Created, InternalServerError]:
        # Save data
        try:
            new_role = RoleRepository.create_role(
                name= data.name
            )
        except Exception as e:
            import traceback
            traceback.print_exc()
            return InternalServerError(error=str(e))

        return Created(data={
            'id': new_role.id,
            'name': new_role.name
        })

    @staticmethod
    async def update_role(id: int, data: UpdateRoleRequest)->Union[Ok, NotFound, InternalServerError]:
        try:
            # update data
            updated_role = RoleRepository.update_role(
                id=id,
                name= data.name
            )
        except Exception as e:
            import traceback
            traceback.print_exc()
            return InternalServerError(error=str(e))

        if updated_role:
            return Ok(data={
                'id': updated_role.id,
                'name': updated_role.name
            })
        else:
            return NotFound(message=f'role with id {id} not found')

    @staticmethod
    async def delete_role(id: int)->Union[NoContent, NotFound, InternalServerError]:
        # Save data
        try:
            new_role = RoleRepository.delete_role(
                id=id
            )
        except Exception as e:
            import traceback
            traceback.print_exc()
            return InternalServerError(error=str(e))

        if new_role:
            return NoContent()
        else:
            return NotFound(message=f'role with id {id} not found')
