from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch

from sqlalchemy.exc import IntegrityError
from services.UserServices import UserServices
from models.User import User
from common.responses_services import InternalServerError, NotFound, Ok

class TestUserServices(IsolatedAsyncioTestCase):

    @patch('services.UserServices.UserRepository')
    async def test_get_all_user_success(self, mockUserRepository):
        # Given
        page = 1
        page_size = 5
        input_user = [
            User(id=2, username='beta@local.com', password='HashedPassword', role_id=2),
            User(id=1, username='alpha@local.com', password='HashedPassword', role_id=1)
        ]
        mockUserRepository.get_all_user.return_value = (
            input_user,
            2,
            1 
        )

        # When
        output = await UserServices.get_all_user(page=page, page_size=page_size)

        # Expect
        """
        format output: 
        Ok(data={
            'page': 1,
            'pageSize': 5,
            'totalPage': 1,
            'count: 2,
            'data': [
                {
                    'id': 2,
                    'username': 'beta@local.com',
                    'role_id: 2
                },
                {
                    'id': 1,
                    'username': 'alpha@local.com',
                    'role_id: 1
                },
            ]
        })
        """
        self.assertIsInstance(output, Ok, msg=f'output should be class of common.responses_services.Ok')
        self.assertEqual(output.data['page'], page, msg=f'output page should be {page}')
        self.assertEqual(output.data['pageSize'], page_size, msg=f'output pageSize should be {page_size}')
        self.assertEqual(len(input_user), len(output.data['data']), msg=f'number of data should be 2')
        for item_input, item_output in zip(input_user, output.data['data']):
            self.assertEqual(item_input.id, item_output['id'])
            self.assertEqual(item_input.username, item_output['username'])
            self.assertEqual(item_input.role_id, item_output['role_id'])

    @patch('services.UserServices.UserRepository')
    async def test_get_all_user_error(self, mockUserRepository):
        # Given
        page = 1
        page_size = 5
        mockUserRepository.get_all_user.side_effect = Exception('Database error')

        # When
        output = await UserServices.get_all_user(page=page, page_size=page_size)

        # Expect
        self.assertIsInstance(output, InternalServerError, msg=f'when error occuured should return class of common.responses_services.InternalServerError')
        self.assertEqual(output.error, 'Database error')

    @patch('services.UserServices.UserRepository')
    async def test_get_detail_user_success(self, mockUserRepository):
        # Given
        input_id = 1
        input_username = 'alpha@local.com'
        input_role_id = 1
        def get_detail_user(id:int):
            return User(id=id, username=input_username, role_id=input_role_id)
        mockUserRepository.get_detail_user.side_effect = get_detail_user

        # When
        output = await UserServices.get_detail_user(id=input_id)

        # Expect
        self.assertIsInstance(output, Ok, msg=f'output should be class of common.responses_services.Ok')
        self.assertEqual(output.data['id'], input_id, msg=f'output id should be same like input {input_id}')
        self.assertEqual(output.data['username'], input_username, msg=f'output username should be {input_username}')
        self.assertEqual(output.data['role_id'], input_role_id, msg=f'output pageSize should be {input_role_id}')

    @patch('services.UserServices.UserRepository')
    async def test_get_detail_user_not_found(self, mockUserRepository):
        # Given
        input_id = 1
        mockUserRepository.get_detail_user.return_value = None

        # When
        output = await UserServices.get_detail_user(id=input_id)

        # Expect
        self.assertIsInstance(output, NotFound, msg=f'output should be class of common.responses_services.NotFound')

    @patch('services.UserServices.UserRepository')
    async def test_get_detail_user_error(self, mockUserRepository):
        # Given
        input_id = 1
        mockUserRepository.get_detail_user.side_effect = Exception('database Error')

        # When
        output = await UserServices.get_detail_user(id=input_id)

        # Expect
        self.assertIsInstance(output, InternalServerError, msg=f'output should be class of common.responses_services.InternalServerError')
        