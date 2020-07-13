from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from user import RegisterUser
from items import Item, Items

app = Flask(__name__)
app.secret_key = 'longcopmplicatedkey'
api = Api(app)
jwt = JWT(app, authenticate, identity)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')
api.add_resource(RegisterUser, '/register')

app.run(port=5000, debug=True)
