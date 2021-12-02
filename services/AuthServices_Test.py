from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch
from common.responses_services import Ok, BadRequest, InternalServerError
from models.Role import Role
from models.User import User
from schemas.AuthSchemas import LoginRequest, LoginResponse, LogoutRequest, LogoutResponse
from services.AuthServices import AuthServices

class TestAuthServices(IsolatedAsyncioTestCase):

    @patch('services.AuthServices.UserRepository')
    @patch('services.AuthServices.validated_user_password')
    @patch('services.AuthServices.generate_jwt_token_from_user')
    async def test_login_success(self, mock_generate_jwt_token_from_user, mock_validated_user_password, mockUserRepository):
        # given
        # user login with correct password
        request = LoginRequest(username='test@local.com', password='correct password')
        mockUserRepository.get_detail_user_from_username_with_role.return_value = User(
            id=1, username='test@local.com', role_id=1, role=Role(id=1, name='admin')
        )
        mock_validated_user_password.return_value = True
        mock_generate_jwt_token_from_user.return_value = 'fakejwttoken'

        # when
        output = await AuthServices.login(request)

        # expect
        self.assertIsInstance(output, Ok, 
            msg='login success should return Ok()')
        output = output.data
        expect = LoginResponse(id=1, username='test@local.com', role={'id': 1, 'name': 'admin'}, token='fakejwttoken').dict()
        self.assertEqual(output['id'], expect['id'], msg=f'json format should use AuthSchema.LoginResponse and output: {expect}')
        self.assertEqual(output['username'], expect['username'], msg=f'json format should use AuthSchema.LoginResponse and output: {expect}')
        self.assertEqual(output['token'], expect['token'], msg=f'json format should use AuthSchema.LoginResponse and output: {expect}')
        self.assertEqual(output['role']['id'], expect['role']['id'], msg=f'json format should use AuthSchema.LoginResponse and output: {expect}')
        self.assertEqual(output['role']['name'], expect['role']['name'], msg=f'json format should use AuthSchema.LoginResponse and output: {expect}')

    @patch('services.AuthServices.UserRepository')
    @patch('services.AuthServices.validated_user_password')
    @patch('services.AuthServices.generate_jwt_token_from_user')
    async def test_login_failed(self, mock_generate_jwt_token_from_user, mock_validated_user_password, mockUserRepository):
        # given
        # User login with incorrect password
        request = LoginRequest(username='test@local.com', password='incorrect password')
        mockUserRepository.get_detail_user_from_username_with_role.return_value = User(
            id=1, username='test@local.com', role_id=1, role=Role(id=1, name='admin')
        )
        mock_validated_user_password.return_value = False
        mock_generate_jwt_token_from_user.return_value = 'fakejwttoken'

        # when
        output = await AuthServices.login(request)

        # expect
        self.assertIsInstance(output, BadRequest, 
            msg='login with incorrect password should return Badrequest()')

    @patch('services.AuthServices.UserRepository')
    @patch('services.AuthServices.validated_user_password')
    @patch('services.AuthServices.generate_jwt_token_from_user')
    async def test_login_user_not_found(self, mock_generate_jwt_token_from_user, mock_validated_user_password, mockUserRepository):
        # given
        # User login with incorrect username
        request = LoginRequest(username='notindatabase@local.com', password='incorrect password')
        mockUserRepository.get_detail_user_from_username_with_role.return_value = None
        mock_validated_user_password.return_value = False
        mock_generate_jwt_token_from_user.return_value = 'fakejwttoken'

        # when
        output = await AuthServices.login(request)

        # expect
        # BadRequest
        self.assertIsInstance(output, BadRequest, 
            msg='login when user not found should return Badrequest()')

    @patch('services.AuthServices.UserRepository')
    @patch('services.AuthServices.validated_user_password')
    @patch('services.AuthServices.generate_jwt_token_from_user')
    async def test_login_error(self, mock_generate_jwt_token_from_user, mock_validated_user_password, mockUserRepository):
        # given
        # database error
        request = LoginRequest(username='notindatabase@local.com', password='incorrect password')
        mockUserRepository.get_detail_user_from_username_with_role.side_effect = Exception('Database Error')
        mock_validated_user_password.return_value = False
        mock_generate_jwt_token_from_user.return_value = 'fakejwttoken'

        # when
        output = await AuthServices.login(request)

        # expect
        # InternalServerError
        self.assertIsInstance(output, InternalServerError, 
            msg='login when user not found should return InternalServerError()')

    @patch('services.AuthServices.get_user_from_jwt_token')
    async def test_logout_success(self, mock_get_user_from_jwt_token):
        # given
        # data correct
        request = LogoutRequest(id=1, username='test@local.com', token='realjwttoken')
        mock_get_user_from_jwt_token.return_value = User(
            id=1, username='test@local.com', password='hashedpassword', role_id=1, role=Role(id=1, name='admin')
        )

        # when
        output = await AuthServices.logout(data=request)

        # expect
        # Ok
        expect = LogoutResponse(id=1, username='test@local.com', role={'id': 1, 'name': 'admin'}).dict()
        self.assertIsInstance(output, Ok, msg='when logout correct should return ok')
        self.assertEqual(output.data['id'], expect['id'])
        self.assertEqual(output.data['username'], expect['username'])
        self.assertEqual(output.data['role']['id'], expect['role']['id'])
        self.assertEqual(output.data['role']['name'], expect['role']['name'])

    @patch('services.AuthServices.get_user_from_jwt_token')
    async def test_logout_failed(self, mock_get_user_from_jwt_token):
        # given
        # data incorrect
        request = LogoutRequest(id=1, username='test@local.com', token='realjwttoken')
        mock_get_user_from_jwt_token.return_value = None

        # when
        output = await AuthServices.logout(data=request)

        # expect
        # BadRequest
        self.assertIsInstance(output, BadRequest, msg='when logout incorrect token should return BadRequest')

    @patch('services.AuthServices.get_user_from_jwt_token')
    async def test_logout_error(self, mock_get_user_from_jwt_token):
        # given
        # database error
        request = LogoutRequest(id=1, username='test@local.com', token='realjwttoken')
        mock_get_user_from_jwt_token.side_effect = Exception('Database Error')

        # when
        output = await AuthServices.logout(data=request)

        # expect
        # Internal Server error
        self.assertIsInstance(output, InternalServerError, msg='when logout while databae error should return InternalServerError')
