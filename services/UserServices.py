from typing import Union
from common.responses_services import Ok, Created, NoContent, BadRequest, NotFound, InternalServerError
from repository.UserRepository import UserRepository
from serializers.UserSerializers import UserCreateRequest, UserUpdateRequest

class UserServices():

    @staticmethod
    async def get_all_user(page: int, pageSize: int)->Ok:
        users = UserRepository.get_all_user(page=page, pageSize=pageSize)
        return Ok(data={
            'page': page,
            'pageSize': pageSize,
            'totalPage': 1,
            'data': users
        })

    @staticmethod
    async def get_detail_user(id: int)->Union[Ok, NotFound, InternalServerError]:
        user = UserRepository.get_detail_user(id)
        if user == None:
            return NotFound(message=f'user with id {id} not found')
        return Ok(user)

    @staticmethod
    async def create_user(data: UserCreateRequest)->Union[Created, BadRequest, InternalServerError]:
        # validation
        if data.password != data.confirm_password:
            return BadRequest(message="password and confirm password not match")

        # Save data
        new_user = UserRepository.create_user(
            username= data.username,
            password= data.password,
            role_id = data.role_id
        )

        return Created(new_user)

    @staticmethod
    async def update_user(id: int, data: UserUpdateRequest)->Union[Ok, BadRequest, NotFound, InternalServerError]:
        # validation
        ## check is password match
        if data.new_password != data.confirm_new_password:
            return BadRequest(message="new_password and confirm_new_password not match")
        ## check is user exists
        updated_user = UserRepository.get_detail_user(id)
        if updated_user == None:
            return NotFound(message=f'user with id {id} not found')

        # update data
        updated_user = UserRepository.update_user(
            id=id,
            username=data.username,
            password=data.new_password,
            role_id=data.role_id
        )

        return Ok(updated_user)

    @staticmethod
    async def delete_user(id: int)->Union[NoContent, NotFound, InternalServerError]:
        user = UserRepository.get_detail_user(id)
        if user == None:
            return NotFound(message=f'user with id {id} not found')
        user = UserRepository.delete_user(id)
        return NoContent()
