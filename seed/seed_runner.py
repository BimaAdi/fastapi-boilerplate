from seed.seed.RoleSeeder import seed_roles
from seed.seed.UserSeeder import seed_users

def initialize_user():
    print('run initialize_user')
    seed_roles()
    seed_users()
    print('completed')
