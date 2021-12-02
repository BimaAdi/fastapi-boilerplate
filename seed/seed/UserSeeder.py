from seed.factory.UserFactory import create_user

def seed_users():
    print('run seed_users')
    create_user('admin@local.com', 'admin', 1)
    create_user('alpha@local.com', '123456', 2)
    create_user('tester@local.com', '123456', 3)
