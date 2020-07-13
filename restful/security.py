from user import User


def authenticate(username, password):
    user = User.find_user(username)
    if user and user.password == password:
        return user


def identity(payload):
    print(payload)
    _id = payload['identity']
    return User.find_user(_id)


