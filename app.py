from flask import Flask

from flask_jwt_extended import JWTManager


app = Flask(__name__)





jwt = JWTManager(app)

if __name__ == '__main__':
    db.init_app(app)


    app.run(port=5000,  debug=True)
