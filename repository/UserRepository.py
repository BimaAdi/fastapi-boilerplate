import math
from typing import Union, Tuple, List
from models import Session
from models.User import User
from sqlalchemy import select, func
from sqlalchemy.orm import joinedload

class UserRepository():

    @staticmethod
    def get_all_user(page:int, page_size:int)->Tuple[List[User], int, int]:
        with Session() as session:
            # get paginated data
            statement = select(User).order_by(User.id.desc())
            if page_size != None:
                statement = statement.limit(page_size)
            if page != None:
                statement = statement.offset((page - 1) * page_size)
            users = session.execute(statement).scalars().all()

            # get count and number page
            statement = select(func.count(User.id))
            num_users = session.execute(statement).scalar()
            num_page = math.ceil(num_users / page_size)

        return (users, num_users, num_page)

    @staticmethod
    def get_detail_user(id:int)->Union[User, None]:
        with Session() as session:
            statement = select(User).where(User.id == id)
            user = session.execute(statement).scalar()
        return user
    
    @staticmethod
    def create_user(username:str, password:str, role_id:int)->Union[User, None]:
        with Session() as session:
            new_user = User(username=username, password=password, role_id=role_id)
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
        return new_user
    
    @staticmethod
    def update_user(id: int, username:str, password:str, role_id:int)->Union[User, None]:
        with Session() as session:
            # check is user exist
            statement = select(User).where(User.id == id)
            user = session.execute(statement).scalar()
            if user == None:
                return None
            # update user
            user.username = username
            user.password = password
            user.role_id = role_id
            session.commit()
            session.refresh(user)

        return user

    @staticmethod
    def delete_user(id:int)->Union[User, None]:
        with Session() as session:
            # check is user exist
            statement = select(User).where(User.id == id)
            user = session.execute(statement).scalar()
            if user == None:
                return None
            session.delete(user)
            session.commit()
        return user
    
    @staticmethod
    def get_detail_user_from_username(username:str)->Union[User, None]:
        with Session() as session:
            statement = select(User).where(User.username == username)
            user = session.execute(statement).scalar()
        return user
    
    @staticmethod
    def get_detail_user_with_role(id:int)->Union[User, None]:
        with Session() as session:
            statement = select(User).options(joinedload(User.role)).where(User.id == id)
            user = session.execute(statement).scalar()
        return user
    