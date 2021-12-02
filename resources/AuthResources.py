from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from common.security import validated_user_password, generate_jwt_token_from_user
from common.responses_schemas import (
    BadRequest, InternalServerError
)
from common.responses_services import common_response
from repository.UserRepository import UserRepository
from schemas.AuthSchemas import LoginRequest, LoginResponse, LogoutRequest, LogoutResponse
from services.AuthServices import AuthServices

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

# for open api login
@router.post('/token')
async def open_api_login(form_data: OAuth2PasswordRequestForm = Depends()):

    user = UserRepository.get_detail_user_from_username_with_role(username=form_data.username)
    if user == None:
        return JSONResponse(content='authorization invalid', status_code=400)
    
    if not validated_user_password(user=user, password=form_data.password):
        return JSONResponse(content='authorization invalid', status_code=400)

    token = generate_jwt_token_from_user(user=user)

    return {"access_token": token, "token_type": "token"}

@router.post('/login', responses={
    '200': {'model': LoginResponse},
    '400': {'model': BadRequest},
    '500': {'model': InternalServerError}
})
async def login(request:LoginRequest):
    result = await AuthServices.login(data=request)
    return common_response(result)

@router.post('/logout', responses={
    '200': {'model': LogoutResponse},
    '400': {'model': BadRequest},
    '500': {'model': InternalServerError}
})
async def logout(request:LogoutRequest):
    result = await AuthServices.logout(data=request)
    return common_response(result)
