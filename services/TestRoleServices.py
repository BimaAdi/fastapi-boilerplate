from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch
from common.responses_services import ( 
    InternalServerError, NoContent, Ok, 
    NotFound, Created
)
from .RoleServices import RoleServices
from models.Role import Role

class TestRoleServices(IsolatedAsyncioTestCase):

    @patch('services.RoleServices.RoleRepository')
    async def test_get_all_roles(self, mockRoleRepository):
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
        
        # should
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
