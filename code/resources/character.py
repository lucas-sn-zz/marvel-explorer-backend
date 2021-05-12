from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource, reqparse
from models.character import CharacterModel
from services.character import UserCharacterServices, MarvelCharacterServices, MarvelCharacterDetailsServices


class UserCharacters(Resource):

    @jwt_required()
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name',
                            required=False,
                            help='This field cannot be empty')

        data = parser.parse_args()
        try:
            characters = UserCharacterServices.get_user_characters_details(
                id_user=get_jwt_identity(), **data)
            return characters, 201
        except Exception as e:
            return {"msg": "An error has occurred ",
                    "error": str(e)}, 500

    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id_character',
                            required=True,
                            help='This field cannot be empty')
        parser.add_argument('name',
                            required=True,
                            help='This field cannot be empty')

        data = parser.parse_args()
        if CharacterModel.find_by_id(id_user=get_jwt_identity(), **data):
            return {'message': f"A character with id {data['id_character']} already exists."}, 400
        character = CharacterModel(id_user=get_jwt_identity(), **data)
        character.save_to_database()
        return {"message": "Character added successfully"}, 201

    @jwt_required()
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id_character',
                            required=True,
                            help='This field cannot be empty')

        data = parser.parse_args()
        if CharacterModel.find_by_id(id_user=get_jwt_identity(), **data) == None:
            return {'message': f"Character not found."}, 400
        character = CharacterModel.find_by_id(
            id_user=get_jwt_identity(), id_character=data['id_character'])
        character.delete_from_database()
        return {"message": "Character deleted"}, 201


class MarvelCharacters(Resource):
    @jwt_required()
    def get(self):
        try:
            characters = MarvelCharacterServices.get_marvel_characters(
                id_user=get_jwt_identity())
            return characters, 201
        except Exception as e:
            return {"msg": "An error has occurred ",
                    "error": str(e)}, 500


class MarvelCharacterDetails(Resource):
    @jwt_required()
    def get(self, id_character):
        character_details = MarvelCharacterDetailsServices.get_marvel_character_details(
            id_user=get_jwt_identity(), id_character=id_character)
        return character_details
