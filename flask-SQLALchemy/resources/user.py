from flask_restful import Resource, reqparse
from models.user import UserModel


class RegisterUser(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help='This field is required')
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help='This field is required')
    created = {'message': 'User created successfully. Welcome!'}
    exists = {'message': 'That username is already in use. Please enter a new one'}

    def post(self):
        data = RegisterUser.parser.parse_args()

        if UserModel.find_user(data['username']):
            return RegisterUser.exists, 400
        # Create user in database.
        user = UserModel(**data, access=1)
        user.save_user()
        return RegisterUser.created, 201
