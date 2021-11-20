from typing import Union

fake_user_data = [
    {
        'id': 1,
        'username': 'alpha@local.com',
        'role_id': 1
    },
    {
        'id': 2,
        'username': 'beta@local.com',
        'role_id': 2
    },
    {
        'id': 3,
        'username': 'beta@local.com',
        'role_id': 3
    },
]

class UserRepository():

    @staticmethod
    def get_all_user(page:int, pageSize:int):
        return fake_user_data

    @staticmethod
    def get_detail_user(id:int)->Union[dict, None]:
        user = [user for user in fake_user_data if user['id'] == id]
        if len(user) == 0:
            return None
        else:
            return user[0]
    
    @staticmethod
    def create_user(username:str, password:str, role_id:int)->Union[dict, None]:
        return {
            'id': 4,
            'username': username,
            'role_id': role_id
        }
    
    @staticmethod
    def update_user(id: int, username:str, password:str, role_id:int)->Union[dict, None]:
        user = [user for user in fake_user_data if user['id'] == id]
        if len(user) == 0:
            return None
        else:
            return {
                'id': 4,
                'username': username,
                'role_id': role_id
            }

    @staticmethod
    def delete_user(id:int)->Union[dict, None]:
        return None
    