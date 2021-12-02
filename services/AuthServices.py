from typing import Union
from common.responses_services import Ok, BadRequest, InternalServerError
from common.security import validated_user_password, generate_jwt_token_from_user, get_user_from_jwt_token
from schemas.AuthSchemas import LoginRequest, LoginResponse, LogoutRequest, LogoutResponse
from repository.UserRepository import UserRepository

class AuthServices():

    @staticmethod
    async def login(data=LoginRequest)->Union[Ok, BadRequest, InternalServerError]:
        try:
            user = UserRepository.get_detail_user_from_username_with_role(username=data.username)
            if user == None:
                return BadRequest(message='Authorization Invalid')
            
            if not validated_user_password(user=user, password=data.password):
                return BadRequest(message='Authorization Invalid')

            token = generate_jwt_token_from_user(user=user)

            result = LoginResponse(
                id=user.id, 
                username=user.username,
                role={
                    'id': user.role.id,
                    'name': user.role.name
                },
                token=token
            )

            return Ok(data=result.dict())
        except Exception as e:
            import traceback
            traceback.print_exc()
            return InternalServerError(error=str(e))

    @staticmethod
    async def logout(data:LogoutRequest)->Union[Ok, BadRequest, InternalServerError]:
        try:
            user = get_user_from_jwt_token(data.token)
            if user != None:
                response = LogoutResponse(
                    id=user.id,
                    username=user.username,
                    role={
                        'id': user.role.id,
                        'name': user.role.name
                    }
                ).dict()
                return Ok(data=response)
            else:
                return BadRequest(message='user not found')
        except Exception as e:
            return InternalServerError(error=str(e))
