from blocklist_logout import BLOCKLIST_LOGOUT
from flask_restful import Resource, reqparse
from models.user import UserModel
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token,get_jwt_identity,jwt_required,get_jwt

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                    type=str,
                    required=True,
                    help="This field cannot be blank."
                    )

_user_parser.add_argument('email',
                    type=str,
                    required=False,
                    help="This field cannot be blank."
                    )
_user_parser.add_argument('password',
                    type=str,
                    required=True,
                    help="This field cannot be blank."
                    )

class UserRegister(Resource):

    def post(self):
        data = _user_parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully."}, 201


class UserLogin(Resource):
    def post(self):
        data = _user_parser.parse_args()

        user = UserModel.find_by_username(data['username'])

        if user and safe_str_cmp(user.password, data['password']):
           #identity will be add the user.id information in JWT
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)

            return {
                'access_token': access_token,
                    'refresh_token': refresh_token

            }, 200

        return {"message": "Invalid Credentials"}, 401

class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']  #jti is the JWT identification
        BLOCKLIST_LOGOUT.add(jti)
        return {"message": "Successfully logged out"}, 200


class UserProfile(Resource):
    @jwt_required()
    def get(self):
        user = UserModel.find_by_id(get_jwt_identity())
        return {
            "usuario": user.username,
            "email": user.email,
            "pass": user.password
                    },200

    @jwt_required()
    def put(self):
        _user_parser = reqparse.RequestParser()

        _user_parser.add_argument('username',
                    type=str,
                    required=False,
                    help="This field cannot be blank."
                    )

        _user_parser.add_argument('email',
                    type=str,
                    required=False,
                    help="This field cannot be blank."
                    )

        _user_parser.add_argument('email',
                            type=str,
                            required=False,
                            help="This field cannot be blank."
                            )
        _user_parser.add_argument('password',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
        _user_parser.add_argument('new_password',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
        data = _user_parser.parse_args()
        user = UserModel.find_by_id(get_jwt_identity())
        print(user.password)
        if user and safe_str_cmp(user.password, data['password']):
            if data['email']:
                user.email = data['email']
            if data['username']:
                user.email = data['email']
            if data['new_password']:
                user.password = data['new_password']
            user.save_to_db()

            jti = get_jwt()['jti']  #jti is the JWT identification
            BLOCKLIST_LOGOUT.add(jti)
            return {"message": "Changes completed successfully. Please log in again"}, 200

        return {"message": "Invalid Credentials!"}, 401