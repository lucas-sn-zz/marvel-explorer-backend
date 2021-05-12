import sqlite3
from flask_restful import Resource, reqparse
from models.comic import ComicModel
from models.marvel import MarvelModel
from services.comic import UserComicServices, MarvelComicServices, MarvelComicDetailsServices
from flask_jwt_extended import get_jwt_identity, jwt_required


class UserComics(Resource):

    @jwt_required()
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name',
                            required=False,
                            type=str,
                            help='This field cannot be empty')
        data = parser.parse_args()

        comics = UserComicServices.get_user_comics_details(
            id_user=get_jwt_identity(), **data)
        return comics, 201

    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id_comic',
                            required=True,
                            type=int,
                            help='This field cannot be empty')
        parser.add_argument('name',
                            required=True,
                            type=str,
                            help='This field cannot be empty')
        data = parser.parse_args()

        if ComicModel.find_by_id(id_user=get_jwt_identity(), id_comic=data['id_comic']):
            return {'message': f"A comic with id {data['id_comic']} already exists."}, 400
        comic = ComicModel(id_user=get_jwt_identity(), **data)
        comic.save_to_database()
        return {"message": "Comic added successfully"}, 201

    @jwt_required()
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id_comic',
                            required=True,
                            help='This field cannot be empty')
        data = parser.parse_args()
        if ComicModel.find_by_id(id_user=get_jwt_identity(), id_comic=data['id_comic']) == None:
            return {'message': f"Comic not found."}, 400
        comic = ComicModel.find_by_id(
            id_user=get_jwt_identity(), id_comic=data['id_comic'])
        comic.delete_from_database()
        return {"message": "Comic deleted"}, 200


class MarvelComics(Resource):
    @jwt_required()
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name',
                            required=False,
                            type=str,
                            help='This field cannot be empty')
        parser.add_argument('page',
                            required=False,
                            type=int,
                            help='This field cannot be empty')

        data = parser.parse_args()
        if data['page'] == None:
            data['page'] = 1

        comics = MarvelComicServices.get_marvel_comics(**data,
                                                       id_user=get_jwt_identity())

        return comics, 200


class MarvelComicDetails(Resource):
    @jwt_required()
    def get(self, id_comic):
        # parser = reqparse.RequestParser()
        comic_details = MarvelComicDetailsServices.get_marvel_comic_details(
            id_user=get_jwt_identity(), id_comic=id_comic)
        return comic_details, 200
