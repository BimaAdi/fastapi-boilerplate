from models import Session
from models.Role import Role

def create_role(name:str)->Role:
    with Session() as session:
        new_role = Role(name=name)
        session.add(new_role)
        session.commit()
        session.refresh(new_role)
    
    return new_role
