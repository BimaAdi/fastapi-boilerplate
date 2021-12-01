from datetime import datetime, timedelta
from typing import Union, Optional
from fastapi import HTTPException
from fastapi.requests import Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param
from pydantic import BaseModel
import bcrypt
from jose import JWTError, jwt
from models.User import User
from repository.UserRepository import UserRepository
from settings import JWT_PREFIX, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

# for edit token authorization prefix
# header Authorization: {JWT_PREFIX} {JWT_TOKEN}
class OAuth2PasswordJWT(OAuth2PasswordBearer):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[dict] = None,
        auto_error: bool = True,
    ):
        super().__init__(
            tokenUrl=tokenUrl,
            scopes=scopes,
            scheme_name=scheme_name,
            auto_error=auto_error,
        )

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme != JWT_PREFIX:
            if self.auto_error:
                raise HTTPException(
                    status_code=401,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": JWT_PREFIX},
                )
            else:
                return None
        return param

oauth2_scheme = OAuth2PasswordJWT(tokenUrl="auth/token")

def generate_hash_password(password:str)->str:
    hash = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())
    return hash.decode()

def validated_user_password(user:User, password:str)->bool:
    return bcrypt.checkpw(password.encode(), user.password.encode())

def generate_jwt_token_from_user(user:User)->str:
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {'id': user.id, 'username': user.username, 'exp': expire}
    jwt_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return jwt_token

def get_user_from_jwt_token(jwt_token:str)->Union[User, None]:
    try:
        payload = jwt.decode(token=jwt_token, key=SECRET_KEY,algorithms=ALGORITHM)
        id = payload.get('id')
        user = UserRepository.get_detail_user_with_role(id=id)
    except JWTError:
        return None
    except Exception as e:
        print(e)
        return None

    return user
