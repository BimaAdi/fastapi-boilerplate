from typing import Union
from sqlalchemy.exc import IntegrityError
from common.responses_services import Ok, Created, NoContent, BadRequest, NotFound, InternalServerError
from common.security import generate_hash_password, validated_user_password
from models.User import User
from repository.UserRepository import UserRepository
from schemas.UserSchemas import UserCreateRequest, UserUpdateRequest

class UserServices():

    @staticmethod
    async def get_all_user(request_user:User, page: int, page_size: int)->Union[Ok, InternalServerError]:
        try:
            users, num_users, num_page = UserRepository.get_all_user(page=page, page_size=page_size)
        except Exception as e:
            return InternalServerError(error=str(e))
        return Ok(data={
            'page': page,
            'pageSize': page_size,
            'totalPage': num_page,
            'data': [{ 'id': item.id, 'username':item.username, 'role_id': item.role_id }for item in users]
        })

    @staticmethod
    async def get_detail_user(request_user:User, id: int)->Union[Ok, NotFound, InternalServerError]:
        try:
            user = UserRepository.get_detail_user(id)
        except Exception as e:
            return InternalServerError(error=str(e))
        
        if user == None:
            return NotFound(message=f'user with id {id} not found')
        return Ok(data={
            'id': user.id,
            'username': user.username,
            'role_id': user.role_id
        })

    @staticmethod
    async def create_user(request_user:User, data: UserCreateRequest)->Union[Created, BadRequest, InternalServerError]:
        # validation
        if data.password != data.confirm_password:
            return BadRequest(message="password and confirm password not match")

        # Hash Password using bcrypt
        data.password = generate_hash_password(data.password)

        # Save data
        try:
            new_user = UserRepository.create_user(
                username= data.username,
                password= data.password,
                role_id = data.role_id
            )
        except IntegrityError as e:
            return BadRequest(message=str(e))
        except Exception as e:
            return InternalServerError(error=str(e))

        return Created(data={
            'id': new_user.id,
            'username': new_user.username,
            'role_id': new_user.role_id
        })

    @staticmethod
    async def update_user(request_user:User, id: int, data: UserUpdateRequest)->Union[Ok, BadRequest, NotFound, InternalServerError]:
        # validation
        ## check is password match
        if data.new_password != data.confirm_new_password:
            return BadRequest(message="new_password and confirm_new_password not match")
        ## check is user exists
        updated_user = UserRepository.get_detail_user(id)
        if updated_user == None:
            return NotFound(message=f'user with id {id} not found')

        ## check is old password match
        if not validated_user_password(updated_user, data.old_password):
            return BadRequest(message="wrong old password")

        # update data
        ## Hash Password using bcrypt
        data.new_password = generate_hash_password(data.new_password)

        ## update data on database
        try:
            updated_user = UserRepository.update_user(
                id=id,
                username=data.username,
                password=data.new_password,
                role_id=data.role_id
            )
        except IntegrityError as e:
            return BadRequest(message=str(e))
        except Exception as e:
            return InternalServerError(error=str(e))

        return Ok(data={
            'id': updated_user.id,
            'username': updated_user.username,
            'role_id': updated_user.role_id
        })

    @staticmethod
    async def delete_user(request_user:User, id: int)->Union[NoContent, BadRequest, NotFound, InternalServerError]:
        try:
            user = UserRepository.delete_user(id)
        except IntegrityError as e:
            return BadRequest(message=str(e))
        except Exception as e:
            return InternalServerError(error=str(e))

        if user == None:
            return NotFound(message=f'user with id {id} not found')
        return NoContent()
