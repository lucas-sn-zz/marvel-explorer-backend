from db import db
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

from flask_jwt_extended import JWTManager
from flask_restful import Api
from resources.user import UserRegister, UserLogin, UserLogout,UserProfile

import os

load_dotenv()

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = os.getenv('FLASK_SECRET_KEY')

api = Api(app)
CORS(app)


jwt = JWTManager(app)

api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')

api.add_resource(UserRegister, '/register')


### routes

@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == '__main__':
    db.init_app(app)


    app.run(port=5000,  debug=True)
