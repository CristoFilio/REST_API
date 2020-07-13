import sqlite3
from flask_restful import Resource, reqparse


class User:
    def __init__(self, _id, username, password, access):
        self.id = _id
        self.username = username
        self.password = password
        self.access = access

    @classmethod
    def find_user(cls, username=None, _id=None):
        """
        Finds the user by username or id in the database.
        It then returns the user or none.
        """
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        if username:
            query = "SELECT * FROM users WHERE username=?"
            result = cursor.execute(query, (username,))
        elif _id:
            query = "SELECT * FROM users WHERE id=?"
            result = cursor.execute(query, (_id,))
        row = result.fetchone()
        if row:
            user = cls(row[0], row[1], row[2], row[3])
        else:
            user = None
        connection.close()
        return user


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
        # Grab the username and pass it to the find user class method.
        data = RegisterUser.parser.parse_args()
        # If user already exists return message and 400.
        if User.find_user(data['username']):
            return RegisterUser.exists, 400
        # Create user in database.
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        new_user = 'INSERT INTO users VALUES (NULL, ?, ?, ?)'
        cursor.execute(new_user, (data['username'], data['password'], 1))

        connection.commit()
        connection.close()
        return RegisterUser.created, 201
