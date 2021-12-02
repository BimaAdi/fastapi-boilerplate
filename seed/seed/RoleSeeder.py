from seed.factory.RoleFactory import create_role

def seed_roles():
    print('run seed_roles')
    create_role('admin')
    create_role('user')
    create_role('tester')
