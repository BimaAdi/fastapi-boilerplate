from os import name
from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch
from common.responses_services import Created, InternalServerError, NotFound, Ok
from serializers.RoleSerializers import CreateRoleRequest
from services.RoleServices import RoleServices
from models.Role import Role

class TestRoleServices(IsolatedAsyncioTestCase):

    @patch('services.RoleServices.RoleRepository')
    async def test_get_all_roles_success(self, mockRoleRepository):
        # given
        page = 1
        page_size = 5
        mockRoleRepository.get_all_roles.return_value = (
            [Role(id=2, name='user'), Role(id=1, name='admin')],
            2,
            1
        )

        # when
        output = await RoleServices.get_all_roles(page=page, page_size=page_size)
        
        # expect
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
                    'name': 'user'
                },
                {
                    'id': 1,
                    'name': 'admin'
                }
            ]
        })
        """
        expected_ouput = {
            'page': 1,
            'pageSize': 5,
            'totalPage': 1,
            'count': 2,
            'data': [
                {
                    'id': 2,
                    'name': 'user'
                },
                {
                    'id': 1,
                    'name': 'admin'
                }
            ]
        }

        self.assertIsInstance(output, Ok, msg=f'output should be class of common.responses_services.Ok')
        self.assertEqual(output.data['page'], 1)
        self.assertEqual(output.data['pageSize'], 5)
        self.assertEqual(output.data['totalPage'], 1)
        self.assertEqual(output.data['count'], 2)
        self.assertIsInstance(output.data['data'], list)
        for index, item in enumerate(expected_ouput['data']):
            self.assertEqual(output.data['data'][index]['id'], item['id'])
            self.assertEqual(output.data['data'][index]['name'], item['name'])

    @patch('services.RoleServices.RoleRepository')
    async def test_get_all_roles_error(self, mockRoleRepository):
        # Given
        page = 1
        page_size = 5
        mockRoleRepository.get_all_roles.side_effect = Exception('Database error')

        # When
        output = await RoleServices.get_all_roles(page=page, page_size=page_size)

        # Expect
        self.assertIsInstance(output, InternalServerError, msg=f'when error occuured should return class of common.responses_services.InternalServerError')
        self.assertEqual(output.error, 'Database error')

    @patch('services.RoleServices.RoleRepository')
    async def test_get_detail_role_success(self, mockRoleRepository):
        # Given
        input_id = 1
        input_name = 'admin'
        def get_detail_role(id:int):
            return Role(id=id, name=input_name)
        mockRoleRepository.get_detail_role.side_effect = get_detail_role

        # When
        output = await RoleServices.get_detail_role(id=input_id)

        # Expect
        self.assertIsInstance(output, Ok, msg=f'output should be class of common.responses_services.Ok')
        self.assertEqual(output.data['id'], input_id, msg=f'output id should be same like input {input_id}')
        self.assertEqual(output.data['name'], input_name, msg=f'output username should be {input_name}')

    @patch('services.RoleServices.RoleRepository')
    async def test_get_detail_role_not_found(self, mockRoleRepository):
        # Given
        input_id = 1
        mockRoleRepository.get_detail_role.return_value = None

        # When
        output = await RoleServices.get_detail_role(id=input_id)

        # Expect
        self.assertIsInstance(output, NotFound, msg=f'output should be class of common.responses_services.NotFound')

    @patch('services.RoleServices.RoleRepository')
    async def test_get_detail_role_error(self, mockRoleRepository):
        # Given
        input_id = 1
        mockRoleRepository.get_detail_role.side_effect = Exception('database Error')

        # When
        output = await RoleServices.get_detail_role(id=input_id)

        # Expect
        self.assertIsInstance(output, InternalServerError, msg=f'output should be class of common.responses_services.InternalServerError')

    @patch('services.RoleServices.RoleRepository')
    async def test_create_role_success(self, mockRoleRepository):
        # Given
        input_name = 'admin'
        input_request = CreateRoleRequest(name=input_name)
        def create_role(name:str):
            return Role(id=1, name=name)
        mockRoleRepository.create_role.side_effect = create_role

        # When
        output = await RoleServices.create_role(data=input_request)

        # Expect
        self.assertIsInstance(output, Created, msg=f'output should be class of common.responses_services.Ok')
        self.assertEqual(output.data['id'], 1, msg=f'output id should be same like input {1}')
        self.assertEqual(output.data['name'], input_name, msg=f'output username should be {input_name}')
