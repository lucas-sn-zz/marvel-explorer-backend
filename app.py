from db import db
from dotenv import load_dotenv
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager


import os

load_dotenv()

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

app.secret_key = os.getenv('FLASK_SECRET_KEY')
api = Api(app)


jwt = JWTManager(app)


### routes

@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == '__main__':
    db.init_app(app)


    app.run(port=5000,  debug=True)
