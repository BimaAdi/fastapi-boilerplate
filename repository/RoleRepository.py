import math
from typing import List, Tuple, Union
from models import Session
from models.Role import Role
from sqlalchemy import select, func

class RoleRepository():

    @staticmethod
    def get_all_roles(page:int, page_size:int)->Tuple[List[Role], int, int]:
        with Session() as session:
            # get paginated data
            statement = select(Role).order_by(Role.id.desc())
            if page_size != None:
                statement = statement.limit(page_size)
            if page != None:
                statement = statement.offset((page - 1) * page_size)
            roles = session.execute(statement).scalars().all()

            # get count and number page
            statement = select(func.count(Role.id))
            num_roles = session.execute(statement).scalar()
            num_page = math.ceil(num_roles / page_size)

        return (roles, num_roles, num_page)

    @staticmethod
    def get_detail_role(id:int)->Union[Role, None]:
        with Session() as session:
            statement = select(Role).where(Role.id == id)
            role = session.execute(statement).scalar()
        return role
    
    @staticmethod
    def create_role(name:str)->Role:
        with Session() as session:
            new_role = Role(name=name)
            session.add(new_role)
            session.commit()
            session.refresh(new_role)
        
        return new_role
        
    
    @staticmethod
    def update_role(id: int, name:str)->Union[Role, None]:
        with Session() as session:
            # check is role exist
            statement = select(Role).where(Role.id == id)
            role = session.execute(statement).scalar()
            if role == None:
                return None
            # update role
            role.name = name
            session.commit()
            session.refresh(role)

        return role

    @staticmethod
    def delete_role(id:int)->Union[Role, None]:
        with Session() as session:
            # check is role exist
            statement = select(Role).where(Role.id == id)
            role = session.execute(statement).scalar()
            if role == None:
                print('role is none')
                return None
            session.delete(role)
            session.commit()
        return role
    