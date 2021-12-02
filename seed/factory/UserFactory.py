from common.security import generate_hash_password
from models import Session
from models.User import User

def create_user(username:str, password:str, role_id:int)->User:
    password = generate_hash_password(password)
    with Session() as session:
        new_user = User(username=username, password=password, role_id=role_id)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
    return new_user
