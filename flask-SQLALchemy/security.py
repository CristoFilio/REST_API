from models.user import UserModel


def authenticate(username, password):
    user = UserModel.find_user(username)
    if user and user.password == password:
        return user


def identity(payload):
    _id = payload['identity']
    return UserModel.find_user(_id=_id)


